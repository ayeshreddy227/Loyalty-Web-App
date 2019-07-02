from pymodm import MongoModel, fields

class Feedback(MongoModel):
    agentId    = fields.ObjectIdField()
    consumerId = fields.ObjectIdField()
    transactionId = fields.ObjectIdField()
    value      = fields.IntegerField()
    message    = fields.CharField(blank=True)
    created_at = fields.DateTimeField()


