


from chalice import Chalice
import json, os

from chalicelib.file_service import process_file
from chalicelib.sqs_service import send_message, get_file_url, get_queue_url_by_name




from dotenv import load_dotenv
load_dotenv()


app = Chalice(app_name='app')


@app.route('/send_file', methods=['POST'])
def send_file():
    queue_url = get_queue_url_by_name(name=os.getenv('QUEUE_NAME'))
    fileUrl = json.dumps(app.current_request.json_body)
    send_message(queue_url=queue_url, message_body=fileUrl)


#
# comment decorator 'on_sqs_message' when run 'pytest test/integration/test_integration.py'
# there is a problem with obligation of parameter 'queue' or 'queue_arn' during to testing
#

@app.on_sqs_message(queue=os.getenv('QUEUE_NAME'))
def handle_sqs_message(event):
    for record in event:
        fileUrl = get_file_url(record.body)
        process_file(fileUrl, os.getenv('bucket_name'))

