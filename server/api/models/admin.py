from pymodm import  MongoModel, fields
import pymongo
#
# time =

class Admin(MongoModel):
    email               = fields.EmailField(required=True)
    password            = fields.CharField(required=True)
    name                = fields.CharField(required=True)
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    class Meta:
        indexes = [
            pymongo.IndexModel([('email', pymongo.ALL)],
                               name="AdminEmailUniqueIndex",
                               unique=True
                               )]

class gg(MongoModel):
    created_at = fields.DateTimeField()

    class Meta:
        indexes = [
            pymongo.IndexModel([('created_at', pymongo.ALL)],
                               name="created_attesting",
                               expireAfterSeconds=10

                               )]
# import datetime
# dd = gg(created_at=datetime.datetime.utcnow()).save()
# import time
# time.sleep(8)
# dd.created_at = datetime.datetime.utcnow() +datetime.timedelta(minutes=10)
# dd.save()


                # asd= rest.objects.raw({'location': {'$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates', [-122.406417,37.785834])])), ('$maxDistance', 500)])}})
# asd = rest.objects.raw({"location":{"$near": {"$geometry": {"type":"Point","coordinates":[-122.406417,37.785834]},"$maxDistance":500}}})
# for i in asd:
#     print i._data