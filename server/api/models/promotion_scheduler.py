from pymodm import MongoModel, fields


class PromotionsScheduler(MongoModel):
    offerId = fields.ObjectIdField()
    scheduler_at = fields.DateTimeField()
    agentId = fields.ObjectIdField()



# asd= rest.objects.raw({'location': {'$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates', [-122.406417,37.785834])])), ('$maxDistance', 500)])}})
# asd = rest.objects.raw({"location":{"$near": {"$geometry": {"type":"Point","coordinates":[-122.406417,37.785834]},"$maxDistance":500}}})
# for i in asd:
#     print i._data