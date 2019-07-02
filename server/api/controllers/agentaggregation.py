from api.models.agents import Agents
from api.controllers.consumeragent import getConsumerAgentByConsumerId
from api.libraries.utilities import getObjectAsDict,removeAdditionalData
from geopy.geocoders import Nominatim

def getAgentByLocation(lat,long,skip,limit,id):
    agentsData = []
    lat = float(lat)
    long = float(long)
    skip = int(skip)
    limit = int(limit)

    # geolocator = Nominatim()
    # location = geolocator.reverse(str(lat)+", "+str(long))
    # location.address.split(',')[0]

    # agents = Agents.objects.raw({"location": { "$geoWithin": { "$centerSphere": [ [ lat, long ], 10/3963.2 ] } }})
    ### To be done in the future
    # agents = Agents.objects.raw({"location": {"$nearSphere": {
    #  "$geometry": {
    #     "type" : "Point",
    #     "coordinates" : [ long,lat ]
    #  },
    # "$minDistance": 0,
    # "$maxDistance": 10000000000
    # }}})
    agents = Agents.objects.all()
    newRestaurants = {}
    newAgentsResult = []
    try:
        # agents1 = agents.aggregate({"$lookup":{"from":"consumeragent","localField":"_id","foreignField":"agentId","as":"consumeragents"}})
        # agents = agents.aggregate({"$skip":skip},{"$limit":limit})
        if id:
            consumeragentdata = getConsumerAgentByConsumerId(id)
            consumeragentids = {}
            for i in consumeragentdata:
                consumeragentids[i["agentId"]] = i
        else:
            consumeragentdata = []
            consumeragentids = {}
        for i in agents:

            temp = getObjectAsDict(i._data)
            temp = removeAdditionalData(temp)
            temp["consumeragent"] = consumeragentids.get(temp["_id"],{})
            newRestaurants[i.created_at] = temp
            agentsData.append(temp)
        for key, value in sorted(newRestaurants.iteritems(), key=lambda (k, v): (v, k)):
            newAgentsResult.append(value)
    except Exception as e:
        print e
        pass
    return {"agents":agentsData,"location":"Nearby Restaurants","slide":newAgentsResult[:5]}

def searchAgents(search_str,skip,limit,id):
    # search_str = search_str.lower()
    # agents = Agents.objects.raw({"name": {'$regex' : '.*' + search_str + '.*'}})
    agents = Agents.objects.raw({"name": {'$regex' : '.*' + search_str + '.*','$options' : 'i'}})
    agents = agents.aggregate({"$skip": int(skip)}, {"$limit": int(limit)})
    agentsData = []
    if id:
        consumeragentdata = getConsumerAgentByConsumerId(id)
        consumeragentids = {}
        for i in consumeragentdata:
            consumeragentids[i["agentId"]] = i
    else:
        consumeragentdata = []
        consumeragentids = {}
    for i in agents:
        temp = getObjectAsDict(i)
        temp = removeAdditionalData(temp)
        temp["consumeragent"] = consumeragentids.get(temp["_id"], {})
        agentsData.append(temp)
    print agentsData
    return {"agents":agentsData}