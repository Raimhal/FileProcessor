import os

from chalice import Chalice
from dotenv import load_dotenv

from chalicelib.core import deserialize
from chalicelib.services.logger_service import log_detections

load_dotenv()

app = Chalice(app_name='logs')

@app.on_sqs_message(queue=os.getenv('RESPONSE_QUEUE_NAME'))
def handle_sqs_detections(event):
    for record in event:
        log_detections(print, deserialize(record.body))