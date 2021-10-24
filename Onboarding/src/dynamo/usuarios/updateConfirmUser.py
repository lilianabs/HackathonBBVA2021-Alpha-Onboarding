import base64
import hashlib
import hmac
import os
import time

import boto3

USER_POOL_ID = os.environ['USER_POOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

def get_secret_hash(usuario):
    mensaje = usuario + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
                   msg=str(mensaje).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2

def updateConfirm(correo):
    dynamodb = boto3.resource('dynamodb')
    timestamp = str(time.time())
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_USUARIOS'])
    response = table.update_item(
        Key={
            'id': get_secret_hash(correo)
        },
        UpdateExpression="set verificado = :v, actualizado = :a",
        ExpressionAttributeValues={
            ':v': True,
            ':a': timestamp
        },
        ReturnValues="ALL_NEW"
    )
    return response