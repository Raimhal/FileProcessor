from chalice import Chalice
import os

from chalicelib.core import get_file_url
from chalicelib.core.convertors import deserialize
from chalicelib.services.file_service import upload_file
from chalicelib.services.logger_service import log
from chalicelib.services.ocr_service import do_photo_ocr
from chalicelib.services.sqs_service import send_message, get_queue_url_by_name


from dotenv import load_dotenv
load_dotenv()


app = Chalice(app_name='app')


@app.route('/send_file', methods=['POST'])
def send_file():
    queue_url = get_queue_url_by_name(name=os.getenv('QUEUE_NAME'))
    url = get_file_url(app.current_request.json_body)
    file_name = upload_file(url, os.getenv('bucket_name'))
    send_message(queue_url=queue_url, message_body=file_name)

#
# comment decorator 'on_sqs_message' when run 'pytest test/integration/test_integration.py'
# there is a problem with obligation of parameter 'queue' or 'queue_arn' during to testing
#

@app.on_sqs_message(queue=os.getenv('QUEUE_NAME'))
def handle_sqs_message(event):
    response_queue_url = get_queue_url_by_name(os.getenv('RESPONSE_QUEUE_NAME'))
    bucket_name = os.getenv('bucket_name')
    for record in event:
        do_photo_ocr(photo=record.body, bucket_name=bucket_name, queue_url=response_queue_url)


@app.on_sqs_message(queue=os.getenv('RESPONSE_QUEUE_NAME'))
def handle_sqs_logs(event):
    for record in event:
        log(print, deserialize(record.body))
# core => sqs => process => sqs => core