import os
import boto3


rekognition = boto3.client('rekognition')

def compareFaces(event, context):
    bucket_name = os.environ['S3_BUCKET_DOCUMENTOS']
    event = event.get('body')
    correo = event['correo']
    correo, dominio = correo.split("@")
    correo = correo + "-" + dominio
    id = correo + "/id.png"
    selfie = correo + "/selfie.png"
    response = rekognition.compare_faces(
    SourceImage={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': id
        }
    },
    TargetImage={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': selfie
        }
    },
    SimilarityThreshold=90,
    QualityFilter='HIGH'
    )
    return response

