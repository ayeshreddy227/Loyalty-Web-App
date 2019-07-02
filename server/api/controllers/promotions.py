from api.models.promotions import Promotions
from api.controllers.offers import getOfferObjById,getOffersIdForSchedulerRemainder,getOfferByBirthday
from api.libraries.utilities import *
from bson import ObjectId
from datetime import timedelta
import pytz
from api.controllers.offers import getOfferIdByDay
from api.controllers.login import getLoginBytokenId,getAllLogin,Login
from api.controllers.consumeragent import ConsumerAgent
from api.controllers.consumers import getBirthdayConsumers
from __init__ import push_service
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()
sched.start()
import datetime
from datetime import timedelta

def getAllPromotionsPerAgent(id):
    allPromotions = []
    promotions = Promotions.objects.raw({"agentId":ObjectId(id)})
    for i in promotions:
        allPromotions.append(getObjectAsDict(i._data))
    return allPromotions

def getAllPromotionsPerAgentForAnalytics(id):
    allPromotions = []
    promotions = Promotions.objects.raw({"agentId":ObjectId(id)})
    for i in promotions:
        temp = i._data
        temp["_id"] = str(temp["_id"])
        allPromotions.append(temp)
    return allPromotions

def getPresentPromotionsPerAgent(id):
    presentPromotions = []
    current_date = datetime.datetime.now()
    promotions =Promotions.objects.raw({"agentId":ObjectId(id),'valid_from': {"$lte":current_date},'valid_to': {"$gte":current_date}})
    for i in promotions:
        promotion_val = getObjectAsDict(i._data)
        promotion_val['valid_from_date'] = i._data['valid_from'].strftime("%d %b")
        promotion_val['valid_to_date'] = i._data['valid_to'].strftime("%d %b")
        promotion_val['valid_from_time'] = i._data['valid_from'].strftime("%I:%M %p")
        promotion_val['valid_to_time'] = i._data['valid_to'].strftime("%I:%M %p")
        expiry_days = (i._data['valid_to']-datetime.datetime.now()).days
        expiry_hours = int((i._data['valid_to']-datetime.datetime.now()).seconds/3600)
        if expiry_days>=1:
            promotion_val['expiresin'] = expiry_days
            promotion_val['expiry_msg'] = "expires in "+str(expiry_days)+" days"
        else:
            promotion_val['expiresin'] = i._data['valid_to'].strftime("%I:%M %p")
            promotion_val['expiry_msg'] = "expires in " + str(expiry_hours) + " hours"
        presentPromotions.append(promotion_val)
    return {"promotions":presentPromotions}

def getPresentPromotionsForConsumer(id):
    presentPromotions = []
    current_date = datetime.datetime.now()
    promotions =Promotions.objects.raw({"consumerId":ObjectId(id),'valid_from': {"$lte":current_date},'valid_to': {"$gte":current_date}})
    for i in promotions:
        promotion_val = getObjectAsDict(i._data)
        promotion_val['valid_from_date'] = i._data['valid_from'].strftime("%d %b")
        promotion_val['valid_to_date'] = i._data['valid_to'].strftime("%d %b")
        promotion_val['valid_from_time'] = i._data['valid_from'].strftime("%I:%M %p")
        promotion_val['valid_to_time'] = i._data['valid_to'].strftime("%I:%M %p")
        expiry_days = (i._data['valid_to']-datetime.datetime.now()).days
        expiry_hours = int((i._data['valid_to']-datetime.datetime.now()).seconds/3600)
        if expiry_days>=1:
            promotion_val['expiresin'] = expiry_days
            promotion_val['expiry_msg'] = "expires in "+str(expiry_days)+" days"
        else:
            promotion_val['expiresin'] = i._data['valid_to'].strftime("%I:%M %p")
            promotion_val['expiry_msg'] = "expires in " + str(expiry_hours) + " hours"
        presentPromotions.append(promotion_val)
    return {"promotions":presentPromotions}


def pushSchedulerRemainder():
    OfferData = getOffersIdForSchedulerRemainder()
    agentIds = []
    agentIdsMap = {}
    for i in OfferData:
        consumerIds = []
        consumer_fcmIds = []
        promotions = []
        agentIds.append(str(i["agentId"]))
        # agentIdsMap[str(i['agentId'])].append(i)
        qs = ConsumerAgent.objects.raw({"agentId": i["agentId"]})
        consumerAgentData = qs.aggregate({ "$project": {"agentId": 1, "consumerId": 1, "dateDifference": {"$divide": [
            {"$subtract": [datetime.datetime.now(), "$updated_at"]}, 1000 * 60 * 60 * 24]}}}
        )
        for k in consumerAgentData:
            if k["dateDifference"] and int(k['dateDifference'])%i["promotion_data"]["schedulerduration"] == 0:
                consumerIds.append({"tokenId":k['consumerId']})
        if consumerIds:
            consumerData = Login.objects.raw({"$or":consumerIds})
            for row in consumerData:
                logininfo = row._data
                if logininfo['fcmId'] not in consumer_fcmIds:
                    promotions.append(
                        Promotions(agentId=i['agentId'], consumerId=logininfo['tokenId'], offerId=i["_id"],
                                   valid_from=i["valid_from"], valid_to=i["valid_to"]))
                    consumer_fcmIds.append(logininfo['fcmId'])
                    try:
                        push_service.notify_single_device(logininfo['fcmId'], message_title=i["name"],
                                                          message_body=i["promotion_data"]["description"],
                                                          color="#FFD085")
                    except:
                        pass
            if promotions:
                Promotions.objects.bulk_create(promotions)
# pushSchedulerRemainder()
def pushBirthdayPromotions():
    consumersData = getBirthdayConsumers()
    if not consumersData:
        return
    consumerIdMap = {}
    consumers = []
    for i in consumersData:
        consumerIdMap[i['_id']] = i['name']
        consumers.append(str(i['_id']))
    offers = []
    consumer_fcmIds = []
    agentOfferMap = {}
    offers = getOfferByBirthday()
    for i in offers:
        agentIds = []
        consumerData = []
        consumer_fcmIds = []
        promotions = []
        offerData = getObjectAsDict(i._data)
        if offerData['offer_type'] == 'promotions' and offerData['promotion_data'].get("birthdayenabled",False):

            try:
                agentOfferMap[i.agentId].append(i)
            except:
                agentOfferMap[i.agentId] = i
            for k in consumers:
                agentIds.append({"agentId":i.agentId,"consumerId":ObjectId(k)})
    # agentIds = list(set(agentIds))
        if agentIds:
            qs = ConsumerAgent.objects.raw({"$or": agentIds})
            consumerData = qs.aggregate(
                {"$lookup": {"from": "login", "localField": "consumerId", "foreignField": "tokenId", "as": "logindata"}})
        for row in consumerData:
            for logininfo in row.get("logindata", []):
                if not logininfo['fcmId'] in consumer_fcmIds:
                    promotions.append(Promotions(agentId=row['agentId'],consumerId=logininfo['tokenId'],offerId=agentOfferMap[row['agentId']]._id,
                                         valid_from=i.valid_from,valid_to=i.valid_to))

                    consumer_fcmIds.append(logininfo['fcmId'])
                    try:
                        name = consumerIdMap.get(str(row['consumerId']),"")
                        msg_title = "Happy Birthday "+name+" !"
                        push_service.notify_single_device(logininfo['fcmId'],message_title=msg_title,message_body=i.promotion_data["description"],         color="#FFD085")
                    except:
                        pass
        if promotions:
            Promotions.objects.bulk_create(promotions)
    consumer_fcmIds = list(set(consumer_fcmIds))
    message_title = ""
    message_body = ""
    data_message = ""
    # push_service.notify_multiple_devices(registration_ids=consumer_fcmIds, message_title=message_title,
    #                                      message_body=message_body, data_message=data_message)
    # startBirthdayPromotions()
# pushBirthdayPromotions()
def pushPromotions():
    OfferId = getOfferIdByDay()
    offers = []

    for i in OfferId:
        offers.append(getOfferObjById(i))
    for i in offers:
        agentIds = []
        consumerData = []
        consumer_fcmIds = []
        promotions = []
        offerData = getObjectAsDict(i._data)
        if offerData['offer_type'] == 'promotions' and offerData['promotion_data'].get("promotionenabled",False) and offerData['promotion_data'].get("sendto","") == "all":
            if not consumerData:
                consumerData = getAllLogin()
                for row in consumerData:
                    if 'fcmId' in row and 'tokenId' in row and row['fcmId'] not in consumer_fcmIds:
                        promotions.append(Promotions(agentId=i.agentId,consumerId=row['tokenId'],offerId=i._id,valid_from=i.valid_from,valid_to=i.valid_to))
                        # consumer_fcmIds.append(row['fcmId'])
                        consumer_fcmIds.append(row['fcmId'])
                        try:
                            push_service.notify_single_device(row['fcmId'],message_title=i.name,message_body=i.promotion_data["description"],color="#FFD085")
                        except:
                            pass
            consumerData = []
        elif offerData['offer_type'] == 'promotions' and offerData['promotion_data'].get("promotionenabled",False) and offerData['promotion_data'].get("sendto","") == "visited":
            # qs = ConsumerAgent.objects.raw({"agentId":i.agentId})
            agentIds.append({"agentId":i.agentId})
    # agentIds = list(set(agentIds))
        if agentIds:
            qs = ConsumerAgent.objects.raw({"$or": agentIds})
            consumerData = qs.aggregate(
                {"$lookup": {"from": "login", "localField": "consumerId", "foreignField": "tokenId", "as": "logindata"}})
        for row in consumerData:
            for logininfo in row.get("logindata",[]):
                if logininfo['fcmId'] not in consumer_fcmIds:
                    promotions.append(Promotions(agentId=row['agentId'],consumerId=logininfo['tokenId'],offerId=i._id,
                                         valid_from=i.valid_from,valid_to=i.valid_to))
                    consumer_fcmIds.append(logininfo['fcmId'])
                    try:
                        push_service.notify_single_device(logininfo['fcmId'],message_title=i.name,message_body=i.promotion_data["description"],color="#FFD085")
                    except:
                        pass
        if promotions:
            Promotions.objects.bulk_create(promotions)
    message_title = "Promotions"
    message_body = ""
    data_message = ""
    # push_service.notify_multiple_devices(registration_ids=consumer_fcmIds, message_title=message_title,
    #                                      message_body=message_body, data_message=data_message)
    # startPromotions()

# pushPromotions()
def getPromotionById(id):
    try:
        promotions = Promotions.objects.get({"_id":ObjectId(id)})
        promotions = getObjectAsDict(promotions._data)
        return promotions
    except Promotions.DoesNotExist:
        return {"error":True,"message":"ID doesn't exist"}

def getPromotionByIdForUser(id,agentId):
    current_date = datetime.datetime.now()
    try:
        qs = Promotions.objects.raw({"_id":ObjectId(id),"agentId":ObjectId(agentId),'valid_from': {"$lte":current_date},'valid_to': {"$gte":current_date}})
        for i in qs:
            promotions = getObjectAsDict(i._data)
            return {"promotions":[promotions]}
    except Promotions.DoesNotExist:
        return {"error":True,"message":"ID doesn't exist"}

def createPromotions(body,id):
    agentId    = ObjectId(id)
    promotion_type = body.get("promotion_type","")
    promotion_data = body.get("promotion_data","")
    consumerId = body.get("consumerId")
    offerId = body.get("offerId")
    name = body.get("name","")
    name = body.get("name","")
    if "T" in body.get("valid_from"):
        body["valid_from"] = body["valid_from"].split("T")[0]
    if "T" in body.get("valid_to"):
        body["valid_to"] = body["valid_to"].split("T")[0]
    valid_from = datetime.datetime.strptime(body.get("valid_from"),"%Y-%m-%d")
    valid_to   = datetime.datetime.strptime(body.get("valid_to"),"%Y-%m-%d")
    promotions = Promotions(consumerId=ObjectId(consumerId),offerId=ObjectId(offerId),name=name,agentId=agentId,promotion_type=promotion_type,promotion_data=promotion_data,valid_from=valid_from,valid_to=valid_to).save()
    promotions = getObjectAsDict(promotions._data)
    return promotions

def updatePromotions(id,body):
    try:
        promotions = Promotions.objects.raw({"_id":ObjectId(id),"agentId":ObjectId(body["agentId"])})[0]
        promotions.promotion_type = body.get("promotion_type", promotions.promotion_type)
        promotions.name = body.get("name", promotions.name)
        promotions.promotion_data = body.get("promotion_data", promotions.promotion_data)
        if "T" in body.get("valid_from",""):
            body["valid_from"] = body["valid_from"].split("T")[0]
        if "T" in body.get("valid_to",""):
            body["valid_to"] = body["valid_to"].split("T")[0]
        if "valid_from" in body:
            promotions.valid_from = datetime.datetime.strptime(body.get("valid_from"), "%Y-%m-%d")
            # promotions.valid_from = promotions.valid_from + td(days=1)
        if "valid_to" in body:
            promotions.valid_to = datetime.datetime.strptime(body.get("valid_to"),"%Y-%m-%d")
            # promotions.valid_to = promotions.valid_to + td(days=1)
        promotions.save()
        promotions = getObjectAsDict(promotions._data)
        return promotions
    except Exception as e:
        print e
        return {"error":True,"message":"incorrect datetime format"}

def deletePromotions(id):
    try:
        Promotions.delete(Promotions(_id=ObjectId(id)))
        return {"message":"Promotions Deleted"}
    except:
        pass


def startPromotions():
    current_date = datetime.datetime.now()
    timedeltaval = 24
    scheduledTimes = [18,16,12]
    nextslot = scheduledTimes[-1]
    for i in scheduledTimes:
        if i>=current_date.hour:
            nextslot = i
            timedeltaval = 0

    scheduletime = datetime.datetime.strptime((current_date+timedelta(hours=timedeltaval)).strftime("%Y-%m-%dT")+str(nextslot),"%Y-%m-%dT%H")
    aa = sched.add_job(pushPromotions, run_date=scheduletime, args=[])
def startBirthdayPromotions():
    current_date = datetime.datetime.now()
    if current_date.hour < 7:
        b_timedelta = 0
    else:
        b_timedelta = 24
    birthdayscheduletime = datetime.datetime.strptime(
        (current_date + timedelta(hours=b_timedelta)).strftime("%Y-%m-%dT") + str(7), "%Y-%m-%dT%H")

    aa = sched.add_job(pushBirthdayPromotions, run_date=birthdayscheduletime, args=[])
# pushPromotions()
# pushBirthdayPromotions()
# startPromotions()
# startBirthdayPromotions()