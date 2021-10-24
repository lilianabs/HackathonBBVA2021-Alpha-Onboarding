import base64
import hashlib
import hmac
import os

import boto3

from src.dynamo.usuarios.updateConfirmUser import updateConfirm

USER_POOL_ID = os.environ['USER_POOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

#Hash
def get_secret_hash(usuario):
    mensaje = usuario + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
                   msg=str(mensaje).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2

def confirmSignUp(event, context):
    event = event.get('body')
    client = boto3.client('cognito-idp')
    try:
        correo = event['correo']
        codigo = event['codigo']
        response = client.confirm_sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(correo),
            Username=correo,
            ConfirmationCode=codigo,
            ForceAliasCreation=False,
        )

    except client.exceptions.UserNotFoundException:
        return {"error": True,"message": "El usuario no existe"}
    except client.exceptions.CodeMismatchException:
        return {"error": True, "message": "Código de verificación invalido"}

    except client.exceptions.NotAuthorizedException:
        return {"error": True,"message": "El usuario ya esta confirmado"}

    except Exception as e:
        return {"error": True, "message": f"Error desconocido {e.__str__()} "}
    updateConfirm(correo)
    return {"error": False,
            "success": True,
            "message": "Has verificado tu cuenta, ahora puedes hacer login.",
            "data": None}