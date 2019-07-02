from pymodm import  MongoModel, fields
import pymongo
#
# time =

class Agents(MongoModel):
    email               = fields.EmailField(required=True)
    password            = fields.CharField(required=True)
    name                = fields.CharField(required=True)
    primary_image       = fields.URLField(required=True)
    background_image    = fields.URLField(required=True)
    location            = fields.PointField(required=True)
    category            = fields.CharField(required=True)
    phone               = fields.CharField(required=True)
    feedback            = fields.FloatField(blank=True)
    totalreviews        = fields.IntegerField(blank=True)
    redeemptstoggle     = fields.BooleanField(required=True)
    starttime           = fields.DateTimeField(required=True)
    endtime             = fields.DateTimeField(required=True)



    #image url , offer template url , location , category , phone ,
    #reward points , offers , punch cards , feedback , birthtday
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        indexes = [
            pymongo.IndexModel([('email', pymongo.ALL)],
                               name="AgentEmailUniqueIndex",
                               unique=True
                               ),
            pymongo.IndexModel([("location", pymongo.GEOSPHERE)]),

            pymongo.IndexModel([('name', pymongo.ALL), ('consumer_id', pymongo.ALL)],
                                   name="NameIndex"
                                   )
        ]  # indexes


# asd= rest.objects.raw({'location': {'$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates', [-122.406417,37.785834])])), ('$maxDistance', 500)])}})
# asd = rest.objects.raw({"location":{"$near": {"$geometry": {"type":"Point","coordinates":[-122.406417,37.785834]},"$maxDistance":500}}})
# for i in asd:
#     print i._data