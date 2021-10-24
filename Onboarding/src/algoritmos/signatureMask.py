import cv2
import boto3
import os
import numpy as np

def signatureMask(event, context):
    s3 = boto3.client("s3")
    event = event['body']
    correo = event['correo']
    correo, dominio = correo.split("@")
    correo = correo + "-" + dominio
    imageKey = correo + "/signature.png"
    bucket_name = os.environ['S3_BUCKET_DOCUMENTOS']
    file_obj = s3.get_object(Bucket=bucket_name, Key=imageKey)
    file_content = file_obj["Body"].read()
    # creating 1D array from bytes data range between[0,255]
    np_array = np.fromstring(file_content, np.uint8)
    # decoding array
    image_np = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # converting image from RGB to Grayscale

    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    result = cv2.bitwise_and(image_np, image_np, mask=thresh)
    result[thresh == 0] = [255, 255, 255]
    cv2.imwrite('/tmp/gray_obj.jpg', result)
    name_file = correo + "/signatureMask.jpg"
    s3.put_object(Bucket= bucket_name, Key=name_file, Body=open("/tmp/gray_obj.jpg", "rb").read())
    return 200




