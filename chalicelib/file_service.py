import logging
import os
import uuid

import boto3
import requests
import mimetypes

from botocore.exceptions import NoCredentialsError
from requests.exceptions import MissingSchema


aws_access_key_id=os.getenv('aws_access_key_id')
aws_secret_access_key=os.getenv('aws_secret_access_key')
region_name=os.getenv('region_name')

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
rekognition = boto3.client('rekognition', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)


def process_file(url, bucket_name):
    try:
        data = requests.get(url, stream=True).raw

        content_type = data.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        file_name = f'{uuid.uuid4()}{extension}'

        save_file(data, bucket_name, file_name)
        detect_text(file_name, bucket_name)

    except MissingSchema as ex:
        print(f"[ERROR] Invalid url '{url}'")
        raise ex
    except FileNotFoundError as ex :
        print("[ERROR] The file was not found")
        raise ex
    except NoCredentialsError as ex:
        print("[ERROR] Credentials not available")
        raise ex
    except Exception as ex:
        print("[ERROR] Something went wrong")
        raise ex


def detect_text(photo, bucket_name):
    response = rekognition.detect_text(Image={'S3Object': {'Bucket': bucket_name, 'Name': photo}})
    textDetections=response['TextDetections']


    if not len(textDetections):
        print(f"Photo '{photo}' doesn't have any text")
        return


    for text in textDetections:
        if text['Type'] != 'LINE':
            continue
        print('-'*100)
        print(f'Text: {text["DetectedText"]}')
        print(f'Confidence: {text["Confidence"]:.2f}%')
        print(f'Type: {text["Type"]}')
    print('-'*100)


def save_file(data, bucket_name, file_name):
    s3.upload_fileobj(data, bucket_name, file_name)
    print(f"File '{file_name}' uploaded successfully")