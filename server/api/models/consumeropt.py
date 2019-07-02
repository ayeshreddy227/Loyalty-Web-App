from pymodm import MongoModel, fields

class consumeropt(MongoModel):
    phone              = fields.CharField(blank=True)
    otp             = fields.CharField(blank=True)

