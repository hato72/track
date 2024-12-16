import base64

def authenticate(auth_header,user):
    try:
        auth_type,value = auth_header.split()
        if auth_type != "Basic":
            return False
        user_id,password = base64.b64decode(value).decode("utf-8").split(":")
        user = user.get_user(user_id)
        return user and user["password"] == password
    except Exception:
        return False
    
def encode_auth(auth_header):
    auth_type,value =auth_header.split()
    if auth_type != "Basic":
        return None
    return base64.b64decode(value).decode("utf-8").split(":")