

from chalice import Chalice

from src.image_service import process_file
from src.sqs_service import get_queue_by_name, send_message, get_file_url
import json, os

from dotenv import load_dotenv
load_dotenv()

app = Chalice(app_name='app')
app.debug = True

QUEUE_NAME = os.getenv('QUEUE_NAME')

queue_url = get_queue_by_name(name=QUEUE_NAME)


@app.on_sqs_message(queue=QUEUE_NAME)
def handle_sqs_message(event):
    for record in event:
        fileUrl = get_file_url(record.body)
        process_file(fileUrl, os.getenv('bucket_name'))


@app.route('/send_file', methods=['POST', 'GET'])
def send_file():
    fileUrl = json.dumps(app.current_request.json_body)
    send_message(queue_url=queue_url, message_body=fileUrl)



