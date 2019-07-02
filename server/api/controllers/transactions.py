from api.models.transactions import Transactions
from api.libraries.utilities import *
import pytz

def createTransaction(body):
    agentId                   = body.get("agentId")
    consumerId                = body.get("consumerId")
    offerId                   = body.get("offerId", "")
    consumeragentId           = body.get("consumeragentId")
    bill                      = body.get("bill",0)
    isFirst                   = body.get("isFirst","")
    redeem_points             = body.get("redeem_points",0)
    created_at                = datetime.datetime.now()

    try:
        if offerId:
            agent=Transactions(redeem_points = redeem_points,agentId=ObjectId(agentId), consumerId=ObjectId(consumerId), offerId=ObjectId(offerId) ,consumeragentId=ObjectId(consumeragentId),
                               bill=bill,isFirst=isFirst,created_at=created_at).save()
        else:
            agent = Transactions(redeem_points=redeem_points, agentId=ObjectId(agentId),
                                 consumerId=ObjectId(consumerId),
                                 consumeragentId=ObjectId(consumeragentId),
                                 bill=bill, isFirst=isFirst, created_at=created_at).save()
        agent=getObjectAsDict(agent._data)
        agent=removeColumnsFromRow(agent)
        return agent
    except Exception as e:
        print e
        return {"error": True}

def getRecentTransactions(consumerId,skip,limit):
    result = []
    try:
        qs = Transactions.objects.raw({"consumerId":ObjectId(consumerId)})
        trasactions = qs.aggregate( {"$limit": 30},{"$lookup":{"from":"agents","localField":"agentId","foreignField":"_id","as":"agentData"}})
        for i in trasactions:
            temp = getObjectAsDict(i)
            temp['agentName'] = temp['agentData'][0]['name']
            temp['date'] = str(i['created_at'].day) + " " + str(i['created_at'].strftime("%b"))
            temp['time'] = i['created_at'].strftime("%I:%M %p")
            result.append(temp)
        result = result[::-1]
    except:
        pass
    return {"transactions":result}

def getRecentTransactionsByAgent(agentId,skip,limit):
    result = []
    try:
        qs = Transactions.objects.raw({"agentId":ObjectId(agentId)})
        trasactions = qs.aggregate({"$limit": 30},{"$lookup":{"from":"consumer","localField":"consumerId","foreignField":"_id","as":"consumerData"}})
        for i in trasactions:
            temp = getObjectAsDict(i)
            temp['consumerName'] = temp['consumerData'][0]['name']
            temp['date'] = str(i['created_at'].day) + " " + str(i['created_at'].strftime("%b"))
            temp['time'] = i['created_at'].strftime("%I:%M %p")
            result.append(temp)
        result = result[::-1]
    except Exception as e:
        pass
    return {"transactions":result}