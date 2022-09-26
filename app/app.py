from chalice import Chalice
from sqs_service import create_queue, send_message
import json, os

from dotenv import load_dotenv
load_dotenv()

app = Chalice(app_name='app')
app.debug = True

@app.route('/send_file', methods=['POST', 'GET'])
def send_file():
    fileUrl = json.dumps(app.current_request.json_body)
    queue = create_queue(name=os.getenv('QUEUE_NAME'))
    send_message(queue=queue, message_body=fileUrl)


@app.on_sqs_message(queue=os.getenv('QUEUE_NAME'), batch_size=1)
def handle_sqs_message(event):
    for record in event:
        app.log.debug("Received message with contents: %s", record.body)