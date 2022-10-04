import os

from chalice import Blueprint

from chalicelib.core import deserialize
from chalicelib.services.logger_service import log_detections
from chalicelib.services.sqs_service import get_queue_url_by_name
from chalicelib.services.ocr_service import do_photo_ocr

events = Blueprint(__name__)

@events.on_sqs_message(queue=os.getenv('RESPONSE_QUEUE_NAME'))
def handle_sqs_detections(event):
    for record in event:
        log_detections(print, deserialize(record.body))
        

@events.on_sqs_message(queue=os.getenv('QUEUE_NAME'))
def handle_sqs_message(event):
    response_queue_url = get_queue_url_by_name(os.getenv('RESPONSE_QUEUE_NAME'))
    bucket_name = os.getenv("BUCKET_NAME")
    for record in event:
        do_photo_ocr(photo=record.body, bucket_name=bucket_name, queue_url=response_queue_url)

