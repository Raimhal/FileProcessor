import os

from chalice import Chalice

from dotenv import load_dotenv

from chalicelib.services.ocr_service import do_photo_ocr
from chalicelib.services.sqs_service import get_queue_url_by_name

load_dotenv()


app = Chalice(app_name='processors')


@app.on_sqs_message(queue=os.getenv('QUEUE_NAME'))
def handle_sqs_message(event):
    response_queue_url = get_queue_url_by_name(os.getenv('RESPONSE_QUEUE_NAME'))
    bucket_name = os.getenv('bucket_name')
    for record in event:
        do_photo_ocr(photo=record.body, bucket_name=bucket_name, queue_url=response_queue_url)


# app >> sqs >> rekognition >> sqs >> log >> app