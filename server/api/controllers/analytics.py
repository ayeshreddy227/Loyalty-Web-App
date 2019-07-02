from collections import OrderedDict
from transactions import *
from api.models.feedback import Feedback
from api.models.consumeragent import ConsumerAgent
from datetime import timedelta as td
from offers import getAllOffersPerAgentForAnalytics
import math
import pytz


def roundup(x):
    roundupval = int(math.ceil(x / 10.0)) * 10
    if roundupval == int(x):
        roundupval = int(roundupval*6/5)
    if int(roundupval) == 0:
        roundupval = 10
    return roundupval
def getDateRanges(startdate, enddate):
    # print startdate, enddate
    d1 = datetime.datetime.strptime(startdate, "%d/%m/%Y")
    d2 = datetime.datetime.strptime(enddate, "%d/%m/%Y")
    d2 = d2 + td(days=1) # Add 24 hours to the end date so it considers todays date.
    return d1,d2


def totalUsers(id):
    totalUsersCount = ConsumerAgent.objects.raw({"agentId":ObjectId(id)}).count()
    return {"total_users":totalUsersCount}

def totalUserByWeek(id):
    today = datetime.datetime.now()
    thisweek  = today.isocalendar()[1] - 1
    thisweekusers = 0
    lastweekusers = 0
    startdate = today + td(days=-today.weekday())
    startdate = startdate - td(days = 7)
    qs = Transactions.objects.raw({"agentId": ObjectId(id),'created_at': {"$gte": startdate, "$lte": today}})
    totalConsumers = qs.aggregate({"$group":{"_id":{"$week":"$created_at"},"totalconsumers":{"$addToSet":"$consumerId"}}},{"$project":{"totalusers":{"$size":"$totalconsumers"}}})
    for i in totalConsumers:
        if i['_id'] == thisweek:
            thisweekusers = i["totalusers"]
        else:
            lastweekusers = i['totalusers']
    if lastweekusers != 0:
        increase_in_users = (thisweekusers - lastweekusers)/lastweekusers
    else:
        increase_in_users = 0
    return {"week_users":thisweekusers,"week_increase_users":increase_in_users}


def totalRevenue(id):
    currentweek = datetime.datetime.now().isocalendar()[1] - 1
    lastweek = (datetime.datetime.now() - td(weeks=1)).isocalendar()[1] -1
    qs = Transactions.objects.raw({"agentId":ObjectId(id)})
    qs = qs.aggregate({"$group":{"_id":{"$week":"$created_at"},"revenue":{ "$sum": "$bill" }}})
    total_revenue = 0
    thisweekrevenue = 0
    lastweekrevenue = 0
    for i in qs:
        total_revenue +=i["revenue"]
        if lastweek == i["_id"]:
            lastweekrevenue = thisweekrevenue
        if currentweek == i["_id"]:
            thisweekrevenue = i["revenue"]
    if lastweekrevenue != 0:
        week_increase_revenue = (thisweekrevenue - lastweekrevenue) / lastweekrevenue
    else:
        week_increase_revenue = 0
    return {"week_revenue":thisweekrevenue,"total_revenue":total_revenue,"week_increase_revenue":week_increase_revenue}

def totalRedeemPoints(id):
    totalRedeems = Transactions.objects.raw({"agentId": ObjectId(id),  "offerId": {'$ne': None}}).count()
    return {"total_transactions":totalRedeems}

def totalTransactionsByWeek(id):
    today = datetime.datetime.now()
    thisweek = today.isocalendar()[1] - 1
    thisweektransactions = 0
    lastweektransactions = 0
    startdate = today + td(days=-today.weekday())
    startdate = startdate - td(days=7)
    qs = Transactions.objects.raw({"agentId": ObjectId(id), "offerId": {'$ne': None},'created_at': {"$gte": startdate, "$lte": today}})
    totalTransactions = qs.aggregate(
        {"$group": {"_id": {"$week": "$created_at"}, "totaltransactions": {"$push": "$consumerId"}}},
        {"$project": {"total": {"$size": "$totaltransactions"}}})
    for i in totalTransactions:
        if i['_id'] == thisweek:
            thisweektransactions = i["total"]
        else:
            lastweektransactions = i['total']
    if lastweektransactions != 0:
        increase_in_transactions = (thisweektransactions - lastweektransactions) / lastweektransactions
    else:
        increase_in_transactions = 0
    return {"week_transactions":thisweektransactions,"week_increase_transactions":increase_in_transactions}



def feedbackLastWeek(id):
    d1 = datetime.datetime.now()
    d2 = d1 - td(days=7)

    qs = Feedback.objects.raw({"agentId": ObjectId(id)})
    rating = qs.aggregate({"$project":{"avg":{"$avg":"$value"}}})
    for i in rating:
        return i["avg"]
    return 0

def newAndReturningUsers(id):
    d1 = datetime.datetime.now()
    d2 = d1 - td(days=7)
    returningUsers = 0
    NewUsers       = 0
    feedbacklastweek = feedbackLastWeek(id)
    qs = Transactions.objects.raw({"agentId":ObjectId(id), 'created_at': {"$gte": d2, "$lte": d1}})
    totalUsersAndReturning = qs.aggregate({"$group":{"_id": {"isFirst": "$isFirst","consumerId":"$consumerId"}}})
    for i in totalUsersAndReturning:
        if i['_id']['isFirst'] == True:
            NewUsers+=1
        else:
            returningUsers+=1
    return {"new_users":NewUsers,"returning_users":returningUsers,"rating":feedbacklastweek}

def totalUsersForMonth(agentId):
    year = datetime.datetime.now().year
    startdate = "01/01/"+str(year)
    enddate = "31/12/"+str(year)
    # enddate = body.get("enddate")
    startdate, enddate = getDateRanges(startdate, enddate)
    qs = Transactions.objects.raw({"agentId": ObjectId(agentId), 'created_at': {"$gte": startdate, "$lte": enddate}})

    months = ["Jan","","Mar","","May","","Jul","","Sep","","Nov",""]
    values = [0]*12
    totalusers = qs.aggregate({"$group": {"_id": {"$month": "$created_at"},"count":{"$addToSet":"$consumerId"}}},{"$project":{"totalusers":{"$size":"$count"}}})

    for i in totalusers:
        values[datetime.datetime.strptime(str(i['_id']), "%m").month-1] = i["totalusers"]

    return {"months":months,"values":values,"max":roundup(float(max(values)))}

def revenueBill(agentId):
    year = datetime.datetime.now().year
    startdate = "01/01/" + str(year)
    enddate = "31/12/" + str(year)
    startdate, enddate = getDateRanges(startdate, enddate)
    day_of_year = startdate.timetuple().tm_yday
    day_of_next_year = enddate.timetuple().tm_yday
    qs = Transactions.objects.raw({"agentId": ObjectId(agentId), 'created_at': {"$gte": startdate, "$lte": enddate}})
    prev = ""
    months = ["Jan","","Mar","","May","","Jul","","Sep","","Nov",""]
    values = [0]*12
    delta = enddate - startdate  # timedelta
    # for i in range(delta.days + 1):
    #     if prev != (startdate + td(days=i)).strftime("%b"):
    #         result[(startdate + td(days=i)).strftime("%b")] = 0
    #         months.append((startdate + td(days=i)).strftime("%b"))
    #         prev = (startdate + td(days=i)).strftime("%b")

    totalusers = qs.aggregate({"$group": {"_id": {"$month": "$created_at"}, "count": {"$sum": "$bill"}}})
    for i in totalusers:
        values[datetime.datetime.strptime(str(i['_id']), "%m").month-1] = i["count"]
    return {"months":months,"values":values,"max":roundup(float(max(values)))}

def totalRewardsBymonth(agentId):
    year = datetime.datetime.now().year
    startdate = "01/01/" + str(year)
    enddate = "31/12/" + str(year)
    startdate, enddate = getDateRanges(startdate, enddate)
    day_of_year = startdate.timetuple().tm_yday
    day_of_next_year = enddate.timetuple().tm_yday
    qs = Transactions.objects.raw({"agentId": ObjectId(agentId), 'created_at': {"$gte": startdate, "$lte": enddate},"offerId":{'$ne':None}})
    months = ["Jan","","Mar","","May","","Jul","","Sep","","Nov",""]
    values = [0]*12
    totalusers = qs.aggregate({"$group": {"_id": {"$month": "$created_at"}, "count": {"$sum": 1}}})
    for i in totalusers:
        values[datetime.datetime.strptime(str(i['_id']), "%m").month-1] = i["count"]
    return {"months":months,"values":values,"max":roundup(float(max(values)))}

def successfullOffer(agentId):
    result = []
    presentOffers = []
    offersmap = {}
    current_date = datetime.datetime.now()
    allOffers = getAllOffersPerAgentForAnalytics(agentId)
    for i in allOffers:
        offersmap[i["_id"]] = i["name"]
        if i["valid_from"]<=current_date<=i['valid_to']:
            presentOffers.append(i)
    offers = {}
    for i in presentOffers:
        offers[i['_id']] = i['name']
    current = []
    qs = Transactions.objects.raw(
        {"agentId": ObjectId(agentId), "offerId": {'$ne': None}})
    totalusers = qs.aggregate({"$group": {"_id": "$offerId", "count": {"$sum": 1}}},{"$sort": {"count": -1}})
    count = 0
    for i in totalusers:
        count+=1
        if i["_id"] in offers.keys():
            current.append({"name":offers[i["_id"]],"count":i['count'],"id":count})
            # offers[i['_id']] = i['count']
        result.append({"name":offersmap[str(i["_id"])],"count":i["count"],"id":count})

    if len(result)>5:
        result = result[:5]
    if len(current)>5:
        current = current[:5]
    if not current:
        current = result
    return {"current":current,"total":result}

def UsersHoldingRewardPoints(agentId):
    label = ["2000+","1500-2000","1000-1500","500-1000","250-500"]
    result = [{"label": "2000+", "count": 0},{"label": "1500-2000", "count": 0},{"label": "1000-1500", "count": 0},{"label": "500-1000", "count": 0},{"label": "250-500", "count": 0}]
    qs = ConsumerAgent.objects.raw(
        {"agentId": ObjectId(agentId)})
    usersrewardpoints = qs.aggregate({ "$project": {"_id": 1,"rewardpoints": 1,
                                 "qtyGte250": { "$and":[{ "$gte" : ["$rewardpoints", 250]},{"$lt":["$rewardpoints",500]}]},
                                 "qtyGte500": { "$and":[{ "$gte" : ["$rewardpoints", 500]},{"$lt":["$rewardpoints",1000]}]},
                                 "qtyGte1000": { "$and":[{ "$gte" : ["$rewardpoints", 1000]},{"$lt":["$rewardpoints",1500]}]},
                                 "qtyGte1500": { "$and":[{ "$gte" : ["$rewardpoints", 1500]},{"$lt":["$rewardpoints",2000]}]},
                                 "qtyGte2000": {"$gte": ["$rewardpoints", 2000]}}},
                                {"$group": {"_id":{"250-500":"$qtyGte250","500-1000":"$qtyGte500","1000-1500":"$qtyGte1000",
                                                   "1500-2000":"$qtyGte1500","2000+":"$qtyGte2000"},"count":{"$sum":1}}})
    for i in usersrewardpoints:
        for k,v in i["_id"].items():
            if v == True:
                index = label.index(k)
                result[index]['count'] = i["count"]
    return {"userholding":result}
