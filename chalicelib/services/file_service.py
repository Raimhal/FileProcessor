import os
import uuid

import boto3
import requests
import mimetypes

from botocore.exceptions import NoCredentialsError
from requests.exceptions import MissingSchema


aws_access_key_id=os.getenv('aws_access_key_id')
aws_secret_access_key=os.getenv('aws_secret_access_key')
region_name=os.getenv('region_name')

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)


def upload_file(url, bucket_name):
    try:
        data = requests.get(url, stream=True).raw

        content_type = data.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        file_name = f'{uuid.uuid4()}{extension}'

        s3.upload_fileobj(data, bucket_name, file_name)
        print(f"File '{file_name}' uploaded successfully")

        return file_name

    except MissingSchema as ex:
        print("[ERROR] Invalid url")
        raise ex
    except FileNotFoundError as ex :
        print("[ERROR] The file was not found")
        raise ex
    except NoCredentialsError as ex:
        print("[ERROR] Credentials not available")
        raise ex
    except Exception as ex:
        print("[ERROR] Something went wrong")
        raise ex