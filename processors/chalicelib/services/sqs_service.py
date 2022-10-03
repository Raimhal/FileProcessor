
import os

import boto3
from botocore.exceptions import ClientError

aws_access_key_id=os.getenv('aws_access_key_id')
aws_secret_access_key=os.getenv('aws_secret_access_key')
region_name=os.getenv('region_name')

sqs = boto3.client('sqs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)


def create_queue(name, attributes=None):
    if not attributes:
        attributes = {}

    try:
        queue = sqs.create_queue(
            QueueName=name,
            Attributes=attributes
        )
        print("Created queue '%s' with URL=%s", name, queue['QueueUrl'])
    except ClientError as error:
        print("[ERROR] Couldn't create queue named '%s'.", name)
        raise error
    except Exception as ex:
        print("[ERROR] '%s'", ex)
        raise ex
    else:
        return queue['QueueUrl']


def get_queue_url_by_name(name):
    try:
        return sqs.get_queue_url(QueueName=name)['QueueUrl']
    except:
        return create_queue(name=name, attributes={'VisibilityTimeout': "120"})


def send_message(queue_url, message_body, message_attributes=None):
    if not message_attributes:
        message_attributes = {}

    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageAttributes=message_attributes
        )
        print("Send message successful: %s", message_body)
    except ClientError as error:
        print("[ERROR] Send message failed: %s", message_body)
        raise error
    except Exception as ex:
        print(f"[ERROR] {ex}")
        raise ex
    else:
        return response