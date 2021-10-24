import boto3
from src.dynamo.key.guardarKeyid import guardarKey
import boto3


client = boto3.client('kms')
#KeyUsage='SIGN_VERIFY',

def createKey(event, context):
    event = event.get('body')
    correo = event['correo']
    response = client.create_key(
        Description=correo,
        Origin='AWS_KMS',
        BypassPolicyLockoutSafetyCheck=False,
        MultiRegion=False
    )
    metadata = response.get('KeyMetadata')
    keyId = metadata.get('KeyId')

    guardarKey(keyId, correo)
    return {"error": False,
            "success": True,
            "message": "Llave creada con exito",
            "data": None}

