import base64
import json
import os

import boto3

# Create an S3 client
s3 = boto3.client('s3')
bucket_name = os.environ['S3_BUCKET_DOCUMENTOS']


s3 = boto3.client('s3')
def uploadId(event, context):
    if event['method'] == 'POST' :
        event = event.get('body')
        name = event['name']
        correo = event['correo']
        correo, dominio = correo.split("@")
        correo = correo + "-" + dominio
        image = event['file']
        image = image[image.find(",")+1:]
        path = correo + "/" + name;
        dec = base64.b64decode(image + "===")
        s3.put_object(Bucket=bucket_name, Key=path, Body=dec)
        return {'statusCode': 200, 'body': json.dumps({'message': 'successful lambda function call'}), 'headers': {'Access-Control-Allow-Origin': '*'}}

