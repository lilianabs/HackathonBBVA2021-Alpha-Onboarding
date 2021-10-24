import base64
import hashlib
import hmac
import os

import boto3

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


def initiate_auth(client, usuario, password):
    secret_hash = get_secret_hash(usuario)
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': usuario,
                'SECRET_HASH': secret_hash,
                'PASSWORD': password,
            },
            ClientMetadata={
                'username': usuario,
                'password': password,
            })
    except client.exceptions.NotAuthorizedException:
        return None, "Usuario o contraseña incorrecto"
    except client.exceptions.UserNotConfirmedException:
        return None, "El usuario no esta confirmado"
    except Exception as e:
        return None, e.__str__()
    return resp, None


def login(event, context):
    event = event.get('body')
    client = boto3.client('cognito-idp')
    for field in ["username", "password"]:
        if event.get(field) is None:
            return {"error": True,
                    "success": False,
                    "message": f"{field} is required",
                    "data": None}
    usuario = event['username']
    password = event['password']
    resp, msg = initiate_auth(client, usuario, password)
    if msg != None:
        return {'message': msg,
                "error": True, "success": False, "data": None}
    if resp.get("AuthenticationResult"):
        return {'message': "success",
                "error": False,
                "success": True,
                "data": {
                    "id_token": resp["AuthenticationResult"]["IdToken"],
                    "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
                    "access_token": resp["AuthenticationResult"]["AccessToken"],
                    "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
                    "token_type": resp["AuthenticationResult"]["TokenType"]
                }
                }
