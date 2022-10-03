import jwt

def decode_jwt(token):
    try:
        return jwt.decode(token, algorithms=["RS256"], options={"verify_signature": False})
    except UnicodeDecodeError as ex:
        raise ex