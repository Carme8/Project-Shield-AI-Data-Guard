from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elbv2,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_wafv2 as wafv2,
    aws_kms as kms,
    aws_iam as iam,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_cloudtrail as cloudtrail,
    aws_events as events,
    aws_events_targets as targets,
    aws_codepipeline as codepipeline,
    aws_backup as backup,
)
from constructs import Construct

class ProjectShieldMasterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ========================================================================
        # 1. NETWORK & VPC
        # ========================================================================
        vpc = ec2.Vpc(self, "SecureVPC",
            max_azs=2,
            nat_gateways=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
                ec2.SubnetConfiguration(name="Private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24)
            ]
        )

        vpc.add_flow_log("FlowLogS3", destination=ec2.FlowLogDestination.to_s3())

        vpc.add_interface_endpoint("SecretsManagerEndpoint", service=ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER)
        vpc.add_interface_endpoint("KmsEndpoint", service=ec2.InterfaceVpcEndpointAwsService.KMS)
        vpc.add_gateway_endpoint("S3Endpoint", service=ec2.GatewayVpcEndpointAwsService.S3)
        vpc.add_gateway_endpoint("DynamoDBEndpoint", service=ec2.GatewayVpcEndpointAwsService.DYNAMODB)

        # ========================================================================
        # 2. SECURITY BASE & ENCRYPTION
        # ========================================================================
        kms_key = kms.Key(self, "AppKMSKey", enable_key_rotation=True)

        # ========================================================================
        # 3. STORAGE & DATABASE
        # ========================================================================
        table = dynamodb.Table(self, "AppTable",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            encryption=dynamodb.TableEncryption.CUSTOMER_MANAGED,
            encryption_key=kms_key,
            point_in_time_recovery=True 
        )

        secure_bucket = s3.Bucket(self, "SecureDataBucket",
            encryption=s3.BucketEncryption.KMS,
            encryption_key=kms_key,
            versioned=True,
            object_lock_enabled=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        backup_vault = backup.BackupVault(self, "BackupVault")
        
        backup_plan = backup.BackupPlan.daily_monthly1_year_retention(self, "DailyBackup")
        
        backup_plan.add_selection("Selection",
            resources=[
                backup.BackupResource.from_dynamo_db_table(table),
                backup.BackupResource.from_arn(secure_bucket.bucket_arn)
            ]
        )

        # ========================================================================
        # 4. COMPUTE & CONTAINER
        # ========================================================================
        cluster = ecs.Cluster(self, "AppCluster", vpc=vpc, container_insights=True)
        
        lb = elbv2.ApplicationLoadBalancer(self, "AppALB", vpc=vpc, internet_facing=True)

        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "AIService",
            cluster=cluster,
            cpu=1024,
            memory_limit_mib=2048,
            desired_count=2,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                environment={"TABLE_NAME": table.table_name},
                secrets={}
            ),
            load_balancer=lb,
            open_listener=False
        )
        
        table.grant_read_write_data(fargate_service.task_definition.task_role)
        kms_key.grant_encrypt_decrypt(fargate_service.task_definition.task_role)

        # ========================================================================
        # 5. SERVERLESS & PII REDUCTION (Logica AI)
        # ========================================================================
        

        lambda_code = """
import json
import boto3
import os
import datetime

comprehend = boto3.client('comprehend')
s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def handler(event, context):
    try:
        body = event.get('body', '')
        if not body:
            return {'statusCode': 400, 'body': 'No text provided'}
        
        # Chiama l'AI per trovare dati sensibili (PII)
        response = comprehend.detect_pii_entities(Text=body, LanguageCode='en')
        
        # Oscuramento (Redaction)
        redacted_text = body
        for entity in sorted(response['Entities'], key=lambda x: x['BeginOffset'], reverse=True):
            start = entity['BeginOffset']
            end = entity['EndOffset']
            redacted_text = redacted_text[:start] + f"[{entity['Type']}]" + redacted_text[end:]
            
        # Salvataggio Protetto su S3 (WORM)
        file_name = f"pii_check_{datetime.datetime.now().isoformat()}.txt"
        # Fix per nomi file illegali (rimuove i due punti dal timestamp)
        file_name = file_name.replace(':', '-') 
        
        s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=redacted_text)
        
        return {
            'statusCode': 200, 
            'body': json.dumps({'original': body, 'redacted': redacted_text, 'saved_to': file_name})
        }
    except Exception as e:
        print(e)
        return {'statusCode': 500, 'body': str(e)}
""" 


        pii_lambda = _lambda.Function(self, "PIIReductionHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=_lambda.Code.from_inline(lambda_code), 
            vpc=vpc,
            environment={"BUCKET_NAME": secure_bucket.bucket_name},
            timeout=Duration.seconds(30)
        )
        
        pii_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["comprehend:DetectPiiEntities", "comprehend:StartPiiEntitiesDetectionJob"],
            resources=["*"]
        ))
        secure_bucket.grant_write(pii_lambda)

        # ========================================================================
        # 6. INGRESS & WAF
        # ========================================================================
        api = apigw.LambdaRestApi(self, "FrontDoorAPI",
            handler=pii_lambda,
            proxy=False 
        )
        
        # Metodo ANY per accettare tutto
        api.root.add_method("ANY") 

        web_acl = wafv2.CfnWebACL(self, "SecurityWAF",
            default_action=wafv2.CfnWebACL.DefaultActionProperty(allow={}),
            scope="REGIONAL",
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name="WAFMetrics",
                sampled_requests_enabled=True
            ),
            rules=[
                wafv2.CfnWebACL.RuleProperty(
                    name="AWS-AWSManagedRulesCommonRuleSet",
                    priority=1,
                    statement=wafv2.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                            vendor_name="AWS",
                            name="AWSManagedRulesCommonRuleSet"
                        )
                    ),
                    override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
                    visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name="CommonRules",
                        sampled_requests_enabled=True
                    )
                )
            ]
        )
        
        waf_assoc = wafv2.CfnWebACLAssociation(self, "WAFAssoc",
            resource_arn=api.deployment_stage.stage_arn, 
            web_acl_arn=web_acl.attr_arn
        )

        # ========================================================================
        # 7. MONITORING & ALERTING
        # ========================================================================
        trail = cloudtrail.Trail(self, "AuditTrail", send_to_cloud_watch_logs=True)

        security_topic = sns.Topic(self, "SecurityAlerts")
        security_topic.add_subscription(subs.EmailSubscription("admin@example.com"))

        rule = events.Rule(self, "GuardDutyRule",
            event_pattern=events.EventPattern(
                source=["aws.guardduty"],
                detail_type=["GuardDuty Finding"]
            )
        )
        rule.add_target(targets.SnsTopic(security_topic))