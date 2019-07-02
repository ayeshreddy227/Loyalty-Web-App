API_KEY = "9MSkGq32VLjzs2Sv"
admin_key = "ZtNMc6jd1B5CtD4U"
import api.controllers.login as  authenticationController
import jwt_lib
def getRole(token):
    return jwt_lib.getPayload(token)

def validate(headers,admin=None):
    token = headers.get('token', False)
    key = headers.get('api-key', False)
    role = ''
    # print key, token
    if(not token):
        if(admin and key == admin_key):
            return {'authenticated': True, "role": "anonymous"}
        elif(not admin and key==API_KEY):
            return {'authenticated': True,"role":"anonymous"}
        else:
            return {'authenticated': False}
    else:
        roleInfo = getRole(token)
        if("error" in roleInfo):
            return {'authenticated': False}
        else:
            roleInfo.update({'authenticated': True})
            return roleInfo

def auth_validation(headers):
    try:
        authtoken = jwt_lib.getPayload(headers['auth-token'])["id"]
        if "error" not in authenticationController.getLoginById(authtoken,headers['token']):
            return {}
        else:
            return {"error":True,"code":401,"message":"Not Authorized Please Login"}
    except:
        return {"error": True, "code": 401, "message": "Not Authorized Please Login"}
