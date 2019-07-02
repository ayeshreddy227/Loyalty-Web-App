from api.models.consumeragent import ConsumerAgent
from api.controllers.agents import getAllAgents,updateAgent,getAgentById
from api.controllers.offers import *
from api.controllers.consumers import *
from api.libraries.utilities import *
import pytz
from api.controllers.transactions import createTransaction
from api.controllers.user import getUserById
from bson import ObjectId
# import pyrebase
from __init__ import push_service
# config = {
#     "apiKey": "AIzaSyBLpsSXrB2C0-H1OXMD8xpxA46EWWZhAHo",
#     "authDomain": "testing-c501c.firebaseapp.com",
#     "databaseURL": "https://testing-c501c.firebaseio.com",
#     "projectId": "testing-c501c",
#     "storageBucket": "testing-c501c.appspot.com",
#     "messagingSenderId": "159832973877"
#   }

# firebase = pyrebase.initialize_app(config)
# db = firebase.database()


def getAllConsumersagent(consumerId,platform,agentIds,allagents):
    consumers=[]
    if platform == "phone":
        qs = ConsumerAgent.objects.raw({"phone":consumerId,"agentId": {"$in": [agentIds]}})
        for row in qs:
            consumer = getObjectAsDict(row._data)
            consumer["offers"] = row["agentId"]["offers"]
            consumer["birthday"] = row["agentId"]["offers"]
            consumers.append(consumer)
        return consumers
    elif platform == "facebook":
        qs = ConsumerAgent.objects.raw({"facebookId": consumerId,"agentId": {"$in": [agentIds]}})
        for row in qs:
            consumer = getObjectAsDict(row._data)
            consumer["offers"] = row["agentId"]["offers"]
            consumer["birthday"] = row["agentId"]["offers"]
            consumers.append(consumer)
        return consumers


def getPromotions(consumerId):
    presentOffers = []
    consumeragentMap = {}
    isBirthday = False
    current_date = datetime.datetime.now()
    offers = Offers.objects.raw(
        {'valid_from': {"$lte": current_date}, 'valid_to': {"$gte": current_date},
         "offer_type": "promotions"})
    consumeragent = getConsumerAgentByConsumerId(consumerId)
    consumer = getConsumerById(consumerId)
    date = str(datetime.datetime.strptime(current_date.strftime("%d/%m/%Y"),"%d/%m/%Y"))
    if consumer['birthday'] == date:
        isBirthday = True
    for i in consumeragent:
        consumeragentMap[i['agentId']] = i
    for i in offers:
        offer_val = getObjectAsDict(i._data)
        sendto = offer_val['promotion_data'].get("sendto","")
        birthdayenabled = offer_val['promotion_data'].get("birthdayenabled",False)
        if birthdayenabled and not isBirthday:
            pass
        elif sendto == "visited" and offer_val['agentId'] in consumeragentMap:
            presentOffers.append(offer_val)
        elif sendto == "all":
            presentOffers.append(offer_val)
    return {"promotions":presentOffers}
# getPromotions("5ad3b584ae26282a43bdfef5")
def generateQR(payload):
    return jwt_lib.getToken(payload)

def getConsumerAgentByConsumerId(consumerId):

    consumeragents = []
    try:
        qs = ConsumerAgent.objects.raw({"consumerId": ObjectId(consumerId)})
        for i in qs:
            consumeragents.append(getObjectAsDict(i._data))
        return consumeragents
    except:
        return consumeragents

def getConsumerAgentByConsumerIdAndAgentId(agentId,consumerId):

    consumeragents = []
    try:
        qs = ConsumerAgent.objects.raw({"consumerId": ObjectId(consumerId),"agentId":ObjectId(agentId)})
        for i in qs:
            consumeragents.append(getObjectAsDict(i._data))
        return consumeragents
    except:
        return consumeragents

def getAllAgentswithConsumerdata(consumerId,platform):
    agentids = []
    allagents = getAllAgents()
    for i in allagents:
        agentids.append(i["_id"])
    consumeragent = getAllConsumersagent(consumerId,platform,agentids,allagents)
    consumers = []
    for row in consumeragent:
        consumer = getObjectAsDict(row._data)
        consumers.append(consumer)
    for n in allagents:
        for i in consumers:
            if i["agentId"] == n["_id"]:
                n["rewardpoints"]=i["rewardpoints"]
                n["punchcardnumber"]=i["punchcardnumber"]
                n["offers"]=i["offers"]
                n["birthday"]=i["birthday"]
    return allagents

def createConsumerAgent(body):
    agentId       =body.get("agentId", "")
    consumerId       =body.get("consumerId", "")
    # birthday    =consumerdata.get("birthday","")
    punchcardnumber = body.get("punchcardnumber",{})
    rewardpoints = body.get("rewardpoints",0)
    created_at = datetime.datetime.now()
    updated_at = datetime.datetime.now()
    consumeragent = ConsumerAgent(agentId=agentId,consumerId=consumerId,punchcardnumber=punchcardnumber
                  ,rewardpoints=rewardpoints,created_at=created_at,updated_at=updated_at).save()
    consumeragent = getObjectAsDict(consumeragent._data)
    return consumeragent

def getConsumerAgent(id):
    try:
        consumer_agent = ConsumerAgent.objects.get({"_id":ObjectId(id)})
        consumer_agent = getObjectAsDict(consumer_agent._data)
        return consumer_agent
    except ConsumerAgent.DoesNotExist:
        return {"error":True,"message":"ID doesn't exist"}

def getConsumerAgentByConsumerAndAgent(agentId,consumerId):
    try:
        consumer_agent = ConsumerAgent.objects.get({"agentId":ObjectId(agentId),"consumerId":ObjectId(consumerId)})
        consumer_agent = getObjectAsDict(consumer_agent._data)
        return consumer_agent
    except ConsumerAgent.DoesNotExist:
        return {"error":True,"message":"ID doesn't exist"}


def updateConsumerAgent(id, body):
    consumer_agent = ConsumerAgent.objects.get({'_id': ObjectId(id)})
    consumer_agent.punchcardnumber = body.get("punchcardnumber", consumer_agent.punchcardnumber)
    consumer_agent.rewardpoints = body.get("rewardpoints", consumer_agent.rewardpoints)
    consumer_agent.updated_at = datetime.datetime.now()
    try:
        consumer=consumer_agent.save()
        consumer=getObjectAsDict(consumer._data)
        return consumer
    except Consumer.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}


def generateQRTokenByOffer(offerId,consumerId):
    offers = getOfferById(offerId)
    if not "error" in offers:
        consumer_agent = getConsumerAgentByConsumerAndAgent(offers["agentId"],consumerId)
        if "error" in consumer_agent:
            return {"QRtoken":getToken({"offerId":offers["_id"],"consumer_id":consumerId})}
        else:
            return {"QRtoken":getToken({"consumerAgent":consumer_agent, "offerId": offers["_id"], "consumer_id": consumerId})}
    else:
        return {"error":True,"message":"Offer has expired"}

def mergeOffers(offers,consumer_agent,bill):
    if offers['offer_type'] == "punchcard":
        consumer_agent["punchcardnumber"] = consumer_agent.get("punchcardnumber",{})
        consumer_agent['punchcardnumber']["current"] +=1
        if consumer_agent['punchcardnumber']["current"] == consumer_agent['punchcardnumber']["total"]:
            consumer_agent['punchcardnumber'] = {}
            return {"message" : "punch card"}
        return {"message":"punchcard updated"}
    elif offers["offer_type"] == "rewardpoints":
        consumer_agent["rewardpoints"] = consumer_agent.get("rewardpoints",0)+int(bill)
        consumer_agent['rewardpoints'] -=int(offers["offer_data"]["rewardpoints"])
        updateConsumerAgent(consumer_agent["_id"],consumer_agent)
        # if offers['offers_data']["reward_type"] == "fixed":
        #     consumer_agent['rewardpoints'] +=offers['offers_data']["reward"]
        # else:
        #     consumer_agent["rewardpoints"] +=offers['offers_data']["reward"]*bill/100
        return {"message":"rewardpoints updated"}
    elif offers['offer_type'] == "promotions":
        return {"message":"promotions updated"}


def validateConsumer(token,bill,agentId):
    bill = int(bill)
    agentId = getUserById(agentId)['agentId']
    offer_id = ""
    offers = {}
    consumer_id = ""
    login_id = ""
    consumer_agent_id = ""
    if 'o.' in token:
        offer_id = token.split('o.')[1][:24]
    if 'ca.' in token:
        consumer_agent_id = token.split('ca.')[1][:24]
    if 'c.' in token:
        login_id = token.split('c.')[1][:24]
    loginData = login.getLoginByloginId(login_id)
    consumerObj = getPayload(loginData['token'])
    if consumerObj['role'] != "consumer":
        return {"error":True}
    else:
        consumer_id = consumerObj['id']
    # spend_redeem_points = body.get("apply_reward_points","")
    if not consumer_agent_id:
        dataPayload = {"consumerId":consumer_id,"agentId":agentId}
        consumer_agent = createConsumerAgent(dataPayload)
        isFirst = True
    else:
        consumer_agent = getConsumerAgent(consumer_agent_id)
        isFirst = False
    if offer_id:
        offers = getOfferById(offer_id)
        if "error" not in offers:
            mergeOffers(offers,consumer_agent,bill)
            # updateConsumerAgent(consumer_agent['_id'],consumer_agent)

        else:
            return {"error":True,"message":"Offer has been expired"}

    else:
        if consumer_agent.get('rewardpoints'):
            consumer_agent["rewardpoints"] = consumer_agent.get("rewardpoints", 0) + int(bill)
        else:
            consumer_agent["rewardpoints"] = int(bill)
        updateConsumerAgent(consumer_agent['_id'], consumer_agent)
    transactionData = createTransaction(
        {"isFirst":isFirst,"consumerId": consumer_id, "agentId": agentId, "offerId": offer_id, "consumeragentId": consumer_agent_id,
         "bill": bill,"redeem_points":offers.get("offer_data",{}).get("rewardpoints",0) if offers else 0})
        # fcmid = getConsumerById(consumer_id)['fcm_id']
    message_title = "Offer"
    message_body = "message sent"
    data_message = {"message":"success","transaction_id":transactionData['_id']}
    # result = push_service.notify_single_device(registration_id=loginData['fcmId'], message_title=message_title,message_body=message_body,data_message=data_message)
        # db.child("su").child(str(consumer_id)).push({"message": "Redeem Points updated successfully"})
    return {"message":"Redeem Points updated successfully"}

def clearFirebase(consumerId):
    db.child('su').child(str(consumerId)).remove()
    return {"message":"removed successfully"}

###########################################################################
def getAllOffersForConsumer(consumerId,platform,start,end):
    restaurants=[]
    if platform == "phone":
        qs = ConsumerAgent.objects.raw({"phone": consumerId})
        for row in qs.aggregate({"$sort": {"name": 1}}, {"$skip":start}, {"$limit": end-start}):
            consumer = getObjectAsDict(row)
            consumer["offers"] = row["agentId"]["offers"]
            restaurants.append(consumer)
        return restaurants
    elif platform == "facebook":
        qs = ConsumerAgent.objects.raw({"facebookId": consumerId})
        for row in qs.aggregate({"$sort": {"name": 1}}, {"$skip": start}, {"$limit": end-start}):
            consumer = getObjectAsDict(row)
            consumer["offers"] = row["agentId"]["offers"]
            restaurants.append(consumer)
        return restaurants
    else:
        return {"error":True,"message":"sorry we have only two platforms phone and facebook"}

def validateConsumers(consumerId,agentId,platform,punchcard,offers,birthday,rewardpoints):

    if platform == "phone":
        agentdata = getAgentById(agentId)
        qs = ConsumerAgent.objects.raw({"phone": consumerId,"agentId":agentId})
        if not qs:
            consumerdata = getConsumerByPhone(consumerId)
            offers = createConsumerAgent(consumerdata,agentdata,"phone",{"punch_cards":rewardpoints,"reward_points":punchcard})
        else:
            offers = getObjectAsDict(qs[0]._data)
        punchdiv = offers["punchcardnumber"].split('/')
        punchdiv = str(int(punchdiv[0])+1)+'/'+punchdiv[1]
        if offers["punchcardnumber"] != "False" and eval(punchdiv) == 1:
            return {"punchcard":True,"id":offers["_id"]}
        else:
            pass
    elif platform == "facebook":
        agentdata = getAgentById(agentId)
        qs = ConsumerAgent.objects.raw({"facebookId": consumerId,"agentId":agentId})
        if not qs:
            consumerdata = getConsumerByFacebookId(consumerId)
            offers = createConsumerAgent(consumerdata,agentdata,"facebook",{"punch_cards":rewardpoints,"reward_points":punchcard})
        else:
            offers = getObjectAsDict(qs[0]._data)
        punchdiv = offers["punchcardnumber"].split('/')
        punchdiv = str(int(punchdiv[0]) + 1) + '/' + punchdiv[1]
        if offers["punchcardnumber"] != "False" and eval(punchdiv) == 1:
            return {"punchcard": True,"id":offers["_id"]}
        else:
            pass
    else:
        return {"error": True, "message": "sorry we have only two platforms phone and facebook"}
    temp = {}
    if offers["rewardpoints"]:
        temp["rewardpoints"] = offers["rewardpoints"]
    offerslist = agentdata["offers"]
    for n in offerslist:
        if n["from"]<datetime.datetime.now()<n["to"]:
            temp["offers"] = agentdata["offers"]
            break
        else:
            agentdata["offers"].pop(n)
    if agentdata["offers"] != offerslist:
        updateAgent(offers["_id"],{"offers":agentdata["offers"]})
    temp["id"] = offers["_id"]
    return temp

def OfferSelection(id, agentId,redeem,punchcard):
    punchcardnum = getAgentById(agentId)["punch_cards"]
    if punchcard:
        if punchcardnum:
            updateConsumerAgent(id, {"punchcardnumber": "0/"+punchcardnum,"redeem":redeem},False)
        else:
            updateConsumerAgent(id, {"punchcardnumber": "","redeem":redeem},False)

    else:
        updateConsumerAgent(id,{"redeem":redeem},punchcardnum)
    return {}
