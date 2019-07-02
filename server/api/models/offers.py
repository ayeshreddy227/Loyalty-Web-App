from pymodm import MongoModel, fields
import pymongo

class Offers(MongoModel):
    '''
    if offer_type == rewardpoint:
        offer_data = {"reward_name":"spend 100 and get coke free","reward_points":100,"reward_Info":"coke"}
    '''
    agentId    = fields.ObjectIdField(required=True)
    name       = fields.CharField(required=True)
    offer_type = fields.CharField(required=True)
    offer_data = fields.DictField(blank=True)
    promotion_data = fields.DictField(blank=True)
    scheduled_at = fields.DateTimeField(blank=True)
    valid_from = fields.DateTimeField(required=True)
    valid_to   = fields.DateTimeField(required=True)
    class Meta:
        indexes = [
            pymongo.IndexModel([('agentId', pymongo.ALL)],
                               name="OffersagentIdIndexField"
                               ),
            pymongo.IndexModel([('valid_from', pymongo.ALL)],
                               name="OffersvalidFromIndexField"
                               ),
            pymongo.IndexModel([('valid_to', pymongo.ALL)],
                               name="OffersvalidToIndexField"
                               )
        ]  # indexes


# asd= rest.objects.raw({'location': {'$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates', [-122.406417,37.785834])])), ('$maxDistance', 500)])}})
# asd = rest.objects.raw({"location":{"$near": {"$geometry": {"type":"Point","coordinates":[-122.406417,37.785834]},"$maxDistance":500}}})
# for i in asd:
#     print i._data