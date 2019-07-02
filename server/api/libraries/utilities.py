import json
from bson import ObjectId
import jwt_lib
import datetime
import dateutil.parser


def convertDatetime(datestring):
    yourdate = datetime.datetime.strptime(datestring[:-8],"%Y-%m-%dT%H:%M")+datetime.timedelta(hours=5,minutes=30)
    return yourdate.strftime("%Y-%m-%dT%H:%M")
def removeColumnsFromRow(row):
    row.pop("password",None)
    return row

def removeAdditionalData(row):
    row.pop("password",None)
    row.pop("email",None)
    row.pop("phone",None)
    row.pop("password",None)
    row.pop("password",None)
    row.pop("password",None)
    return row

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

def encode(data):
    return JSONEncoder().encode(data)

def decode(data):
    return json.JSONDecoder().decode(data)

def getObjectAsDict(data):
    # combines the above 2 functions in one call
    return decode(encode(data))

from math import sin, cos, sqrt, atan2, radians


# approximate radius of earth in km
def get_distancebetween2latlong():
    R = 6373.0

    lat1 = radians(52.2296756)
    lon1 = radians(21.0122287)
    lat2 = radians(52.406374)
    lon2 = radians(16.9251681)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    print distance
# get_distancebetween2latlong()