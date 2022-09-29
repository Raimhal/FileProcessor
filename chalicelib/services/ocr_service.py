import json
import os

import boto3

from chalicelib.core.convertors import serialize
from chalicelib.services.sqs_service import send_message

aws_access_key_id=os.getenv('aws_access_key_id')
aws_secret_access_key=os.getenv('aws_secret_access_key')
region_name=os.getenv('region_name')

rekognition = boto3.client('rekognition', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)


def do_photo_ocr(photo, bucket_name, queue_url):
    detections = detect_text(photo, bucket_name)

    if not len(detections):
        print(f"Photo '{photo}' doesn't have any text")
        return

    send_message(queue_url=queue_url, message_body=serialize(detections))


def detect_text(photo, bucket_name):
    response = rekognition.detect_text(Image={'S3Object': {'Bucket': bucket_name, 'Name': photo}})
    return response['TextDetections']