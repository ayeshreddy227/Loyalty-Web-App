from api.models.promotion_scheduler import PromotionsScheduler
from api.libraries.utilities import *
from bson import ObjectId


def getPromotionsScheduler(agentId):
    promotions = []
    promotion_scheduler = PromotionsScheduler.objects.raw({"agentId":ObjectId(agentId)})
    for i in promotion_scheduler:
        promotions.append(getObjectAsDict(i._data))
    return promotions



def createPromotionsScheduler(body,id):
    agentId    = ObjectId(id)
    offerId = body.get("offerId")
    scheduled_at = datetime.datetime.strptime(body.get("scheduled_at"),"%Y-%m-%dT%H")
    promotion_scheduler = PromotionsScheduler(agentId=ObjectId(agentId),offerId=ObjectId(offerId),scheduled_at=scheduled_at).save()
    promotion_scheduler = getObjectAsDict(promotion_scheduler._data)
    return promotion_scheduler

def updatePromotionsScheduler(id,body):
    try:
        promotion_scheduler = PromotionsScheduler.objects.raw({"_id":ObjectId(id),"agentId":ObjectId(body["agentId"])})[0]
        promotion_scheduler.offerId = ObjectId(body['offerId']) if body.get("offerId","") else promotion_scheduler.offerId
        promotion_scheduler.scheduled_at = datetime.datetime.strptime(body.get("scheduled_at"), "%Y-%m-%dT%H") if body.get("scheduled_at","") else promotion_scheduler.scheduled_at
        promotion_scheduler.save()
        promotion_scheduler = getObjectAsDict(promotion_scheduler._data)
        return promotion_scheduler
    except Exception as e:
        print e
        return {"error":True,"message":"incorrect datetime format"}

def deletePromotionsSchedulerScheduler(id):
    try:
        PromotionsScheduler.delete(PromotionsScheduler(_id=ObjectId(id)))
        return {"message":"PromotionsScheduler Deleted"}
    except:
        pass