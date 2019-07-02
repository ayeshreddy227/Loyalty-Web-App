from pymodm import MongoModel, fields


class User(MongoModel):
    '''
    if offer_type == rewardpoint:
        offer_data = {"reward_name":"spend 100 and get coke free","reward_points":100,"reward_Info":"coke"}
    '''
    agentId    = fields.ObjectIdField(required=True)
    email      = fields.EmailField(required=True)
    password   = fields.CharField(required=True)
    created_at = fields.DateTimeField(required=True)
    updated_at = fields.DateTimeField(required=True)
