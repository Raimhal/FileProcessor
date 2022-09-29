import json

from chalicelib.core.convertors import deserialize


def get_file_url(data):
    try:
        return data['fileUrl']
    except Exception as ex:
        print("[ERROR] Invalid message body")
        raise ex