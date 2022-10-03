import os

from chalice import Blueprint, CognitoUserPoolAuthorizer, AuthResponse

from chalicelib.core import get_file_url
from chalicelib.services import decode_jwt
from chalicelib.services.file_service import upload_file
from chalicelib.services.sqs_service import get_queue_url_by_name, send_message

sender = Blueprint(__name__)

@sender.authorizer()
def jwt_auth(auth_request):
    token = auth_request.token.replace("Bearer ", "")
    decoded = decode_jwt(token)
    return AuthResponse(routes=['*'], principal_id=decoded['sub'])


@sender.route('/send_file', methods=['POST'], authorizer=jwt_auth)
def send_file():
    queue_url = get_queue_url_by_name(name=os.getenv('QUEUE_NAME'))
    url = get_file_url(sender.current_request.json_body)
    file_name = upload_file(url, os.getenv('bucket_name'))
    send_message(queue_url=queue_url, message_body=file_name)