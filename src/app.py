

from chalice import Chalice

from src.image_service import process_file
from src.sqs_service import get_queue_by_name, send_message, receive_message
import json, os



from dotenv import load_dotenv
load_dotenv()

app = Chalice(app_name='app')
app.debug = True

QUEUE_NAME = os.getenv('QUEUE_NAME')

queue_url = get_queue_by_name(name=QUEUE_NAME)

@app.route('/receive_file', methods=['POST', 'GET'])
# @app.on_sqs_message(queue=os.getenv('QUEUE_NAME'))
def handle_sqs_message():
    message = receive_message(queue_url=queue_url)
    process_file(message, 'bucket-file-processor')


@app.route('/send_file', methods=['POST', 'GET'])
def send_file():
    fileUrl = json.dumps(app.current_request.json_body)
    send_message(queue_url=queue_url, message_body=fileUrl)



