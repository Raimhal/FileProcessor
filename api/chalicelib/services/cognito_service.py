import os

import boto3
from botocore.exceptions import ClientError

username = "kormish2003@gmail.com"
password = "Epidemic_2021"

client = boto3.client("cognito-idp", region_name=os.getenv("COGNITO_USER_POOL_REGION"))

print(os.getenv("COGNITO_USER_POOL_REGION"))
print(os.getenv("COGNITO_USER_CLIENT_ID"))

def sign_up(data):
    try:
        response = client.sign_up(
            ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
            Username=data['email'],
            Password=data['password'],
            UserAttributes=[{"Name": "email", "Value": data['email']}],
        )
        print(response)
        return response
    except (ClientError, Exception) as ex:
        print(ex)
        raise ex


def confirm_sign_up(data):
    try:
        response = client.confirm_sign_up(
            ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
            Username=data['email'],
            ConfirmationCode=data['code'],
        )
        return response
    except (ClientError, Exception) as ex:
        print(ex)
        raise ex


def sign_in(data):
    try:
        response = client.initiate_auth(
            ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": data['email'], "PASSWORD": data['password']},
        )
        return response["AuthenticationResult"]
    except (ClientError, Exception) as ex:
        print(ex)
        raise ex


