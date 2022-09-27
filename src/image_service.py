import logging
import uuid

import boto3
import requests
import mimetypes

from botocore.exceptions import NoCredentialsError

logger = logging.getLogger(__name__)

s3 = boto3.client('s3', aws_access_key_id='AKIA5TQRTX42YZZM67FY', aws_secret_access_key='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', region_name='eu-west-2')
rekognition = boto3.client('rekognition', aws_access_key_id='AKIA5TQRTX42YZZM67FY', aws_secret_access_key='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', region_name='eu-west-2')


def process_file(url, bucket_name):
    print(url)
    try:
        data = requests.get(url, stream=True).raw

        content_type = data.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        file_name = f'{uuid.uuid4()}{extension}'

        save_file(data, bucket_name, file_name)
        detect_text(file_name, bucket_name)

    except FileNotFoundError as ex :
        logger.exception("The file was not found")
        raise ex

    except NoCredentialsError as ex:
        logger.exception("Credentials not available")
        raise ex


def detect_text(photo, bucket_name):
    response = rekognition.detect_text(Image={'S3Object': {'Bucket': bucket_name, 'Name': photo}})
    textDetections=response['TextDetections']

    if not len(textDetections):
        logger.info(f"Photo '{photo}' doesn't have any text")
        return

    for text in textDetections:
        if text['Type'] != 'LINE':
            continue
        logger.info('-'*60)
        logger.info(f'Text: {text["DetectedText"]}')
        logger.info(f'Confidence: {text["Confidence"]:.2f}%')
        logger.info(f'Type: {text["Type"]}')
    logger.info('-'*60)


def save_file(data, bucket_name, file_name):
    s3.upload_fileobj(data, bucket_name, file_name)
    print(f"File '{file_name}' uploaded successfully")