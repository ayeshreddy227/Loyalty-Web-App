# import facebook
#
# api_key = 'Your App API Key'
# secret  = 'Your App Secret Key'
#
# session_key = 'your infinite Session key of user'
#
# fb = Facebook(api_key, secret)
# fb.session_key = session_key

# now use the fb object for playing around
from api.models.consumer import Consumer
from api.libraries.jwt_lib import *
import login
from api.libraries.utilities import *
from bson import ObjectId
import requests
import pytz

def getAllConsumers():
    consumers=[]
    for row in Consumer.objects.all():
        consumer = getObjectAsDict(row._data)
        consumers.append(consumer)
    return consumers


def getConsumerByPhone(phone):
    try:
        consumer = Consumer.objects.get({"phone": phone})
        return getObjectAsDict(consumer._data),consumer
    except Consumer.DoesNotExist:
        return None,None

def checkphone(phone):
    try:
        consumer = Consumer.objects.get({"phone": phone})
        getObjectAsDict(consumer._data)
        return {"success":True}
    except Consumer.DoesNotExist:
        return {"error":True}
    except Exception as e:
        print e

def getConsumerByFacebookId(facebookId):
    try:
        consumer = Consumer.objects.get({"facebookId": facebookId})
        return getObjectAsDict(consumer._data),consumer
    except Consumer.DoesNotExist:
        return None,None

def getBirthdayConsumers():
    promotions = []
    currentdate = datetime.datetime.now()
    currentdatestr = currentdate.strftime('%d/%m/%Y')
    currentdate = datetime.datetime.strptime(currentdatestr, "%d/%m/%Y")
    promotion_scheduler = Consumer.objects.raw({"birthday": currentdate})
    for i in promotion_scheduler:
        promotions.append(getObjectAsDict(i._data))
    return promotions

def createConsumer(body):
    type       =body.get("type", "")
    consumer_id=body.get("consumer_id","")
    phone      =body.get("phone", "")
    name       =body.get("name","")
    email      =body.get("email","")
    birthday   =body.get("birthday", "")#dd/mm/yyyy
    birthday   =datetime.datetime.strptime(birthday,'%Y-%m-%d')
    created_at =datetime.datetime.now()
    updated_at =datetime.datetime.now()
    try:
    # print AgentId, phone, "Checkpoint Consumer 1"
        consumer = Consumer(type=type,consumer_id=consumer_id,name=name,phone=phone,email=email,birthday=birthday,created_at=created_at,updated_at=updated_at).save()
        return getObjectAsDict(consumer._data)
    except Exception as e:
        print e
        return {"error": True,"message":"Consumer already exist"}
# createConsumer({"phone":"8332811814","name":"Abhiram","birthday":"22/05/1995"})

def loginConsumer(content,platform):
    # facebookResponse = requests.get("https://graph.facebook.com/me/?access_token="+content["token"])
    try:
        consumer = Consumer.objects.get({"consumer_id":content["consumer_id"],"type":platform})
        consumerData = getObjectAsDict(consumer._data)
        consumerData['token'] = getToken({"id": consumerData['_id'], "role": "consumer"})
        loginData = login.createLogin(consumerData['token'],consumerData['_id'], fcmId=content['fcmId'])
        consumerData['auth-token'] = getToken({"id": loginData['_id'], "role": "auth"})
        consumerData['formated_birthday'] = consumer.birthday.strftime("%B").title()+" "+str(consumer.birthday.day)
        consumerData['fcm_id'] =  content['fcmId']
        consumerData['login_id'] = loginData['_id']
        return consumerData
    except:
        return {"error":True,"message":"Invalid Phone Number"}


def getConsumerById(id):
    try:
        consumer=Consumer.objects.get({'_id': ObjectId(id)})
        consumer=getObjectAsDict(consumer._data)
        return consumer
    except Consumer.DoesNotExist:
        return {"error": True, "message": "Consumer does not exist"}


def getConsumerByAgentId(AgentId):
    try:
        consumers=[]
        for consumer in Consumer.objects.raw({"AgentId": ObjectId(AgentId)}):
            consumer=getObjectAsDict(consumer._data)
            consumers.append(consumer)
        # consumers=list(Consumer.objects.raw({"AgentId": ObjectId(AgentId)}))
        return consumers
    except Exception as e:
        print e
        return {"error": True}


def updateConsumer(id, body):
    consumer = Consumer.objects.get({'_id': ObjectId(id)})
    consumer.name       =body.get("name", consumer.name)
    consumer.phone      =body.get("phone", consumer.phone)
    consumer.email      =body.get("email",consumer.email)
    consumer.updated_at = datetime.datetime.now()

    try:
        consumer=consumer.save()
        consumer=getObjectAsDict(consumer._data)
        return consumer
    except Consumer.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}


def deleteConsumer(id):
    try:
        Consumer.delete(Consumer(_id=ObjectId(id)))
        return {"success": True}
    except Consumer.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}
