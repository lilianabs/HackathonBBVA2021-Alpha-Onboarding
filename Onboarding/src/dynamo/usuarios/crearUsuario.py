import base64
import hashlib
import hmac
import os
import time
import boto3
from src.cognito.signUp import signUp

USER_POOL_ID = os.environ['USER_POOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

def get_secret_hash(usuario):
    mensaje = usuario + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
                   msg=str(mensaje).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2

def crearUsuario(event, context):
    dynamodb = boto3.resource('dynamodb')
    timestamp = str(time.time())
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_USUARIOS'])
    event = event['body']
    for field in ["nombre", "apellidos",  "cedCid", "nit", "telefono", "correo",  "password"]:
        if not event.get(field):
            return {"error": False, "success": True, 'message': f"Falta el atributo {field}", "data": None}
    nombre = event['nombre']
    apellidos = event['apellidos']
    cedCid = event['cedCid']
    nit = event['nit']
    telefono = event['telefono']
    correo = event['correo']
    password = event['password']
    item = {
        'id': get_secret_hash(correo),
        'nombre': nombre,
        'apellidos': apellidos,
        'cedCid' : cedCid,
        'nit': nit,
        'telefono': telefono,
        'correo': correo,
        'verificado': False,
        'creado': timestamp,
        'actualizado': timestamp,
    }
    table.put_item(Item=item)
    signUp(nombre, correo, password)
    return {"error": False,
            "success": True,
            "message": "Confirma tu registro, busca en tu correo el codigo de verificación",
            "data": None}