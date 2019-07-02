from pymodm import MongoModel, fields

class Transactions(MongoModel):
    agentId              = fields.ObjectIdField(required=True)
    consumerId           = fields.ObjectIdField(required=True)
    consumeragentId      = fields.ObjectIdField(required=True)
    offerId              = fields.ObjectIdField(blank=True)
    bill                 = fields.IntegerField(blank=True)
    isFirst              = fields.BooleanField(blank=True)
    redeem_points        = fields.IntegerField(blank=True)
    created_at           = fields.DateTimeField(required=True)