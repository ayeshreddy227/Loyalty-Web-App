# from apscheduler.schedulers.background import BackgroundScheduler
# sched = BackgroundScheduler()
# sched.start()
import datetime
s3urls = []
from api.models.background_imgs import Backgroundimages
from api.libraries.utilities import *
import boto3
import pytz
aws_access_key = ""
aws_secret_key = ""
s3 = boto3.client("s3", aws_access_key_id=aws_access_key,
                  aws_secret_access_key=aws_secret_key)
client = boto3.resource("s3", aws_access_key_id=aws_access_key,
                        aws_secret_access_key=aws_secret_key)

# def fetchs3urlsbackground():
all_objects = s3.list_objects(Bucket='pubicbackgroundimages', Prefix='')
temp = []
for i in all_objects['Contents']:
    if i["Key"][-1] != "/":
        s3urls.append("https://s3-ap-south-1.amazonaws.com/pubicbackgroundimages/" + i['Key'])
print(len(s3urls))
    # sched.add_job(fetchs3urlsbackground, run_date=datetime.datetime.now() + datetime.timedelta(minutes=10), args=[])
# aa = sched.add_job(fetchs3urlsbackground, run_date=datetime.datetime.now(), args=[])
# fetchs3urlsbackground()
def getAllbackgroundimages():
    # backgroundimagesdata=[]
    # for row in Backgroundimages.objects.all():
    #     backgroundimages = getObjectAsDict(row._data)
    #     # backgroundimagesdata.append(backgroundimages)
    #     return {"imgs":backgroundimages['urls']}
    return {"imgs":s3urls}



def createBackgroundimages(body):
    url                   = body.get("url")
    name                   = body.get("name")
    created_at              = datetime.datetime.now()
    updated_at              = datetime.datetime.now()
    try:
        backgroundimages=Backgroundimages(url=url, name=name,
                     created_at=created_at,updated_at=updated_at).save()
        backgroundimages=getObjectAsDict(backgroundimages._data)
        return backgroundimages
    except Exception as e:
        print e
        return {"error": True,"message":"Email already exists"}

def updateBackgroundimages(id, body):
    backgroundimages = Backgroundimages.objects.get({"_id":ObjectId(id)})
    backgroundimages.url = body.get("url",backgroundimages.url)
    backgroundimages.name = body.get("name", backgroundimages.email)
    backgroundimages.updated_at = datetime.datetime.now()

    try:
        backgroundimages=backgroundimages.save()
        backgroundimages=getObjectAsDict(backgroundimages._data)
        return backgroundimages
    except Backgroundimages.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}


def deleteBackgroundimages(id):
    try:
        Backgroundimages.delete(Backgroundimages(_id=ObjectId(id)))
        return {"success": True}
    except Backgroundimages.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}
