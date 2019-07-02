import jwt
SECRET_KEY = "GyYNnKhD7WnILt90"
def getToken(payload):

    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def getPayload(token,isAuthToken=None):
    return jwt.decode(token, SECRET_KEY)