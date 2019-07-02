from pymodm import MongoModel, fields

class Backgroundimages(MongoModel):
    urls              = fields.ListField(blank=True)
    name             = fields.CharField(blank=True)
    created_at       = fields.DateTimeField()
    updated_at       = fields.DateTimeField()

