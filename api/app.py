from chalice import Chalice
import os

from chalicelib.core import get_file_url
from chalicelib.services.file_service import upload_file
from chalicelib.services.sqs_service import send_message, get_queue_url_by_name


from dotenv import load_dotenv
load_dotenv()


app = Chalice(app_name='api')


@app.route('/send_file', methods=['POST'])
def send_file():
    queue_url = get_queue_url_by_name(name=os.getenv('QUEUE_NAME'))
    url = get_file_url(app.current_request.json_body)
    file_name = upload_file(url, os.getenv('bucket_name'))
    send_message(queue_url=queue_url, message_body=file_name)


# app >> /send_file >> s3 >> sqs >> app