from pymodm import MongoModel, fields
import pymongo
#
# time =

class Login(MongoModel):
    token      = fields.CharField()
    fcmId      = fields.CharField(blank=True)
    tokenId    = fields.ObjectIdField()
    class Meta:
        indexes = [
            pymongo.IndexModel([('tokenId', pymongo.ALL)],
                               name="LogintokenDIndexField"
                               )
        ]  # indexes

# asd= rest.objects.raw({'location': {'$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates', [-122.406417,37.785834])])), ('$maxDistance', 500)])}})
# asd = rest.objects.raw({"location":{"$near": {"$geometry": {"type":"Point","coordinates":[-122.406417,37.785834]},"$maxDistance":500}}})
# for i in asd:
#     print i._data