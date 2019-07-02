from agents import *

class Consumer(MongoModel):
    type            = fields.CharField(required=True)
    consumer_id     = fields.CharField(required=True)
    email           = fields.EmailField(blank=True)
    name            = fields.CharField(blank=True)
    phone           = fields.CharField(blank=True)
    birthday        = fields.DateTimeField(blank=True)
    created_at      = fields.DateTimeField()
    updated_at      = fields.DateTimeField()
    class Meta:
            indexes = [
                pymongo.IndexModel([('type', pymongo.ALL),('consumer_id', pymongo.ALL)],
                                   name="ConsumerUniqueIndex",
                                   unique = True
                                   )
            ]  # indexes

