import json
import jwt


def get_file_url(data):
    try:
        return data['fileUrl']
    except Exception as ex:
        print("[ERROR] Invalid message body")
        raise ex


def deserialize(data):
    return json.loads(data)


def decode_jwt(token):
    try:
        return jwt.decode(token, algorithms=["RS256"], options={"verify_signature": False})
    except UnicodeDecodeError as ex:
        raise ex