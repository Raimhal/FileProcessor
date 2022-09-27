import json
import logging
import os

import boto3
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
sqs = boto3.client('sqs', aws_access_key_id='AKIA5TQRTX42YZZM67FY', aws_secret_access_key='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', region_name='eu-west-2')


def create_queue(name, attributes=None):
    if not attributes:
        attributes = {}

    try:
        queue = sqs.create_queue(
            QueueName=name,
            Attributes=attributes
        )
        logger.info("Created queue '%s' with URL=%s", name, queue['QueueUrl'])
    except ClientError as error:
        logger.exception("Couldn't create queue named '%s'.", name)
        raise error
    else:
        return queue['QueueUrl']


def get_queue_by_name(name):
    try:
        return sqs.get_queue_by_name(QueueName=name).__dict__['_url']
    except:
        return create_queue(name=os.getenv('QUEUE_NAME'), attributes={'VisibilityTimeout': "120"})

def send_message(queue_url, message_body, message_attributes=None):
    if not message_attributes:
        message_attributes = {}

    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageAttributes=message_attributes
        )
        logger.info("Send message successful: %s", message_body)
    except ClientError as error:
        logger.exception("Send message failed: %s", message_body)
        raise error
    else:
        return response

def receive_message(queue_url):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['All'])
    try:
        return json.loads(response.get('Messages', [])[0]['Body'])['fileUrl']
    except IndexError as ex:
        logger.exception("Queue is empty")
        raise ex
