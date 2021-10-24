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

def signUp(nombre, correo, password):
    client = boto3.client('cognito-idp')
    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(correo),
            Username=correo,
            Password=password,
            UserAttributes=[
                {
                    'Name': "name",
                    'Value': nombre
                },
                {
                    'Name': "email",
                    'Value': correo
                }
            ],
            ValidationData=[
                {
                    'Name': "email",
                    'Value': correo
                },
                {
                    'Name': "custom:username",
                    'Value': correo
                }
            ])


    except client.exceptions.UsernameExistsException as e:
        return {"error": False,
                "success": True,
                "message": "Este correo ya esta registrado",
                "data": None}
    except client.exceptions.InvalidPasswordException as e:

        return {"error": False,
                "success": True,
                "message": "La contraseña debe contener letras mayusculas, minusculas, números y caracteres especiales.",
                "data": None}
    except client.exceptions.UserLambdaValidationException as e:
        return {"error": False,
                "success": True,
                "message": "Este correo ya esta registrado",
                "data": None}

    except Exception as e:
        return {"error": False,
                "success": True,
                "message": str(e),
                "data": None}
    return {"error": False,
            "success": True,
            "message": "Confirma tu registro, busca en tu correo el codigo de validación",
            "data": None}