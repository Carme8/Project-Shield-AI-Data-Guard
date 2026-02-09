import boto3
import json
import os

def handler(event, context):
    comprehend = boto3.client('comprehend')
    
    # Prende il testo dal body della richiesta POST, altrimenti usa un default
    try:
        body = json.loads(event.get('body', '{}'))
        text = body.get('text', "Nessun testo fornito per l'analisi.")
        
        response = comprehend.detect_pii_entities(
            Text=text,
            LanguageCode='it'
        )
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'success',
                'entities_found': len(response['Entities']),
                'entities': response['Entities']
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }