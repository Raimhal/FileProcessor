
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
sqs = boto3.resource('sqs')


def create_queue(name, attributes=None):
    if not attributes:
        attributes = {}

    try:
        queue = sqs.create_queue(
            QueueName=name,
            Attributes=attributes
        )
        logger.info("Created queue '%s' with URL=%s", name, queue.url)
    except ClientError as error:
        logger.exception("Couldn't create queue named '%s'.", name)
        raise error
    else:
        return queue


def send_message(queue, message_body, message_attributes=None):
    if not message_attributes:
        message_attributes = {}

    try:
        response = queue.send_message(
            MessageBody=message_body,
            MessageAttributes=message_attributes
        )
        logger.info("Send message successful: %s", message_body)
    except ClientError as error:
        logger.exception("Send message failed: %s", message_body)
        raise error
    else:
        return response