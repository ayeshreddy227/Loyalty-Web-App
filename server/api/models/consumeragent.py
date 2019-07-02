from agents import *

class ConsumerAgent(MongoModel):
    consumerId          = fields.ObjectIdField()
    agentId             = fields.ObjectIdField()
    # birthday            = fields.CharField(blank=True)
    punchcardnumber     = fields.DictField(blank=True)
    rewardpoints        = fields.IntegerField(blank=True)
    created_at          = fields.DateTimeField()
    updated_at          = fields.DateTimeField()
    class Meta:
        indexes = [
            pymongo.IndexModel([('consumerId', pymongo.ALL),('agentId', pymongo.ALL)],
                               name="ConsumerAgentUniqueIndex",
                               unique=True
                               )]