import os
import aws_cdk as cdk
from shield_stack import ProjectShieldMasterStack

app = cdk.App()

ProjectShieldMasterStack(app, "ProjectShieldMasterStack",
    # Questa configurazione dice al CDK di usare l'account e la regione 
    # configurati nel tuo profilo AWS CLI locale.
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    )
)

app.synth()