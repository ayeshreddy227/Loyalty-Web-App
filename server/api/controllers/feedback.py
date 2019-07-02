from api.models.feedback import Feedback
from api.controllers.agents import updateFeedback
from api.libraries.utilities import *
import pytz

def getAllFeedbackByAgent(id,skip,limit):
    feedback=[]
    qs = Feedback.objects.raw({"agentId": ObjectId(id)})
    # qs = Feedback.objects.raw({"agentId": ObjectId(id)}).limit(limit).skip(
    #                 skip).order_by(
    #                 [("created_at", -1)])
    qs = qs.aggregate({"$sort":{"created_at":-1}},{"$limit":limit},{"$skip":skip},{"$lookup":{"from":"consumer","localField":"consumerId","foreignField":"_id","as":"consumerData"}})
    for row in qs:
        consumerData = row["consumerData"]
        row = getObjectAsDict(row)
        row = removeColumnsFromRow(row)
        if consumerData:
            row['name'] = row['consumerData'][0]['name']
            row['phone'] = row['consumerData'][0]['phone']
        else:
            row['name'] = ""
            row['phone'] = ""
        row.pop("consumerData",None)
        feedback.append(row)
    return {"feedback":feedback}


def createFeedback(body):
    value = body.get("value",0)
    message = body.get("message","")
    agentId = body.get("agentId")
    consumerId = body.get("consumerId")
    transactionId = body.get("transactionId")

    created_at = datetime.datetime.now()
    try:
        feedback=Feedback(agentId=agentId,consumerId=consumerId,transactionId=transactionId,value=value,message=message,created_at=created_at).save()
        updateFeedback(agentId,value)
        feedback=getObjectAsDict(feedback._data)
        return feedback
    except Exception as e:
        print e
        return {"error": True}

def updateFeedbackData(body,id):
    feedbackdata = Feedback.objects.get({"_id":ObjectId(id)})
    feedbackdata.message = body.get("message","")
    try:
        feedbackdata = feedbackdata.save()
        feedbackdata = getObjectAsDict(feedbackdata._data)
        return feedbackdata
    except Exception as e:
        print e
        return {"error": True}

def deleteFeedback(id):
    try:
        Feedback.delete(Feedback(_id=ObjectId(id)))
        return {"success": True}
    except Feedback.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}
