from pymodm import MongoModel, fields


class Promotions(MongoModel):
    '''
    if offer_type == rewardpoint:
        offer_data = {"reward_name":"spend 100 and get coke free","reward_points":100,"reward_Info":"coke"}
    '''
    agentId    = fields.ObjectIdField(required=True)
    consumerId = fields.ObjectIdField(blank=True)
    offerId    = fields.ObjectIdField(blank=True)
    valid_from = fields.DateTimeField(required=True)
    valid_to   = fields.DateTimeField(required=True)



# asd= rest.objects.raw({'location': {'$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates', [-122.406417,37.785834])])), ('$maxDistance', 500)])}})
# asd = rest.objects.raw({"location":{"$near": {"$geometry": {"type":"Point","coordinates":[-122.406417,37.785834]},"$maxDistance":500}}})
# for i in asd:
#     print i._data