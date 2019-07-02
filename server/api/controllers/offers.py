from api.models.offers import Offers
from api.libraries.utilities import *
from bson import ObjectId
from datetime import timedelta as td
import pytz
from api.libraries.utilities import convertDatetime


def getAllOffersPerAgent(id):
    allOffers = []
    offers = Offers.objects.raw({"agentId":ObjectId(id)})
    for i in offers:
        allOffers.append(getObjectAsDict(i._data))
    return allOffers

def getAllOffersPerAgentForAnalytics(id):
    allOffers = []
    offers = Offers.objects.raw({"agentId":ObjectId(id)})
    for i in offers:
        temp = i._data
        temp["_id"] = str(temp["_id"])
        allOffers.append(temp)
    return allOffers



def getOfferIdByDay():
    promotions = []
    currentdate = datetime.datetime.now()
    currentdatestr = currentdate.strftime('%d/%m/%YT%H')
    currentdate = datetime.datetime.strptime(currentdatestr+":00","%d/%m/%YT%H:%M")
    promotion_scheduler = Offers.objects.raw({"scheduled_at":currentdate})
    for i in promotion_scheduler:
        promotions.append(str(i._id))
    return promotions
def getOfferByBirthday():
    offersdata = []
    current_date = datetime.datetime.now()
    offers = Offers.objects.raw(
        { 'valid_from': {"$lte": current_date}, 'valid_to': {"$gte": current_date},
         "promotion_data.birthdayenabled": True})
    return offers


def getOffersIdForSchedulerRemainder():
    promotions = []
    current_date = datetime.datetime.now()
    promotion_scheduler = Offers.objects.raw({"promotion_data.schedulerenabled": True,"promotion_data.schedule_at":str(current_date.hour)})
    for i in promotion_scheduler:
        promotions.append(i._data)
    return promotions

def getPresentOffersPerAgent(id,offer_type="rewardpoints",consumeragentpoints=0):
    presentOffers = []
    current_date = datetime.datetime.now()
    offers =Offers.objects.raw({"agentId":ObjectId(id),'valid_from': {"$lte":current_date},'valid_to': {"$gte":current_date},"offer_type":offer_type})
    for i in offers:
        offer_val = getObjectAsDict(i._data)

        offer_val['valid_from_date'] = i._data['valid_from'].strftime("%d %b")
        offer_val['valid_to_date'] = i._data['valid_to'].strftime("%d %b")
        offer_val['valid_from_time'] = i._data['valid_from'].strftime("%I:%M %p")
        offer_val['valid_to_time'] = i._data['valid_to'].strftime("%I:%M %p")
        expiry_days = (i._data['valid_to']-datetime.datetime.now()).days
        expiry_hours = int((i._data['valid_to']-datetime.datetime.now()).seconds/3600)
        if expiry_days>=1:
            offer_val['expiresin'] = expiry_days
            offer_val['expiry_msg'] = "expires in "+str(expiry_days)+" days"
        else:
            offer_val['expiresin'] = i._data['valid_to'].strftime("%I:%M %p")
            offer_val['expiry_msg'] = "expires in " + str(expiry_hours) + " hours"
        # offer_val['enabled']=True
        presentOffers.append(offer_val)
    arrangedOffers = {}
    finalOffers = []
    nonvalidOffers = []
    if offer_type == "rewardpoints":
        for i in presentOffers:
            if consumeragentpoints>int(i.get("offer_data",{}).get("rewardpoints",0)):
                i['enabled'] = True
                if int(i.get("offer_data",{}).get("rewardpoints",0)) in arrangedOffers:
                    arrangedOffers[int(i.get("offer_data", {}).get("rewardpoints", 0))].append(i)
                else:
                    arrangedOffers[int(i.get("offer_data",{}).get("rewardpoints",0))] = [i]
            else:
                i['enabled'] = False
                nonvalidOffers.append(i)
        arrandedList = arrangedOffers.keys()
        arrandedList.sort(reverse=True)
        for i in arrandedList:
            finalOffers=finalOffers+arrangedOffers[i]
        finalOffers=finalOffers+nonvalidOffers
        return {"offers":finalOffers}
    return {"offers":presentOffers}
# getPresentOffersPerAgent("5aad22ecae2628135a3c621e")
def getOfferById(id):
    try:
        offers = Offers.objects.get({"_id":ObjectId(id)})
        if offers.valid_from <=datetime.datetime.now()<=offers.valid_to:
            offers = getObjectAsDict(offers._data)
            return offers
        else:
            return {"error":True,"message":"ID doesn't exist"}
    except Offers.DoesNotExist:
        return {"error":True,"message":"ID doesn't exist"}

def getOfferObjById(id):
    try:
        offers = Offers.objects.get({"_id":ObjectId(id)})
        # offers = getObjectAsDict(offers._data)
        return offers
    except Offers.DoesNotExist:
        return {"error":True,"message":"ID doesn't exist"}

def getOfferByIdForUser(id,agentId):
    current_date = datetime.datetime.now()
    try:
        qs = Offers.objects.raw({"_id":ObjectId(id),"agentId":ObjectId(agentId),'valid_from': {"$lte":current_date},'valid_to': {"$gte":current_date}})
        for i in qs:
            offers = getObjectAsDict(i._data)
            return {"offers":[offers]}
    except Offers.DoesNotExist:
        return {"error":True,"message":"ID doesn't exist"}

def createOffers(body,id):
    agentId    = ObjectId(id)
    offer_type = body.get("offer_type","")
    offer_data = body.get("offer_data",{})
    promotion_data = body.get("promotion_data",{})
    name = body.get("name","")
    body['valid_from'] = convertDatetime(body['valid_from'])
    body['valid_to'] = convertDatetime(body['valid_to'])
    if "T" in body.get("valid_from"):
        body["valid_from"] = body["valid_from"].split("T")[0]
    if "T" in body.get("valid_to"):
        body["valid_to"] = body["valid_to"].split("T")[0]
    valid_from = datetime.datetime.strptime(body.get("valid_from"),"%Y-%m-%d")
    valid_to   = datetime.datetime.strptime(body.get("valid_to"),"%Y-%m-%d")
    if offer_type == "promotions" and "sendtime" in promotion_data:
        body['scheduled_at'] = convertDatetime(body['scheduled_at'])
        scheduled_at = datetime.datetime.strptime(body['scheduled_at'].split("T")[0] + "T" + promotion_data['sendtime'],
                                   "%Y-%m-%dT%H:%M")
        body['scheduled_at'] = scheduled_at
        offers = Offers(name=name,agentId=agentId,offer_type=offer_type,offer_data=offer_data,scheduled_at=scheduled_at,promotion_data=promotion_data,valid_from=valid_from,valid_to=valid_to).save()
    else:
        offers = Offers(name=name, agentId=agentId, offer_type=offer_type, offer_data=offer_data,
                        promotion_data=promotion_data, valid_from=valid_from,
                        valid_to=valid_to).save()
    offers = getObjectAsDict(offers._data)
    return offers

def updateOffers(id,body):
    try:
        promotion_data = body.get("promotion_data", {})
        offers = Offers.objects.raw({"_id":ObjectId(id),"agentId":ObjectId(body["agentId"])})[0]
        offers.offer_type = body.get("offer_type", offers.offer_type)
        offers.name = body.get("name", offers.name)
        offers.offer_data = body.get("offer_data", offers.offer_data)
        offers.promotion_data = body.get("promotion_data", offers.promotion_data)

        if "T" in body.get("valid_from",""):
            body['valid_from'] = convertDatetime(body['valid_from'])
            body["valid_from"] = body["valid_from"].split("T")[0]
        if "T" in body.get("valid_to",""):
            body['valid_to'] = convertDatetime(body['valid_to'])
            body["valid_to"] = body["valid_to"].split("T")[0]
        if "valid_from" in body:
            offers.valid_from = datetime.datetime.strptime(body.get("valid_from"), "%Y-%m-%d")
            # offers.valid_from = offers.valid_from + td(days=1)
        if "valid_to" in body:
            offers.valid_to = datetime.datetime.strptime(body.get("valid_to"),"%Y-%m-%d")
            # offers.valid_to = offers.valid_to + td(days=1)
        if offers.offer_type == "promotions" and "sendtime" in promotion_data:
            body['scheduled_at'] = convertDatetime(body['scheduled_at'])
            offers.scheduled_at = datetime.datetime.strptime(
                body['scheduled_at'].split("T")[0] + "T" + promotion_data['sendtime'],
                "%Y-%m-%dT%H:%M")
            body['scheduled_at'] = offers.scheduled_at
        offers.save()
        offers = getObjectAsDict(offers._data)
        return offers
    except Exception as e:
        print e
        return {"error":True,"message":"incorrect datetime format"}

def deleteOffers(id):
    try:
        Offers.delete(Offers(_id=ObjectId(id)))
        return {"message":"Offers Deleted"}
    except:
        pass