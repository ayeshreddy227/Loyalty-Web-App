from api.models.agents import Agents
from api.libraries.jwt_lib import *
from api.libraries.utilities import *
import login
import base64,os

import boto3
import pytz
aws_access_key = "AKIAJYAWJ3PRE7QPE6AA"
aws_secret_key = "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"
s3 = boto3.client("s3",aws_access_key_id=aws_access_key,
                               aws_secret_access_key=aws_secret_key)
client = boto3.resource("s3",aws_access_key_id=aws_access_key,
                               aws_secret_access_key=aws_secret_key)

def getAllAgents():
    agents=[]
    for row in Agents.objects.all():
        agent = getObjectAsDict(row._data)
        agent = removeColumnsFromRow(agent)
        agents.append(agent)
    return agents


def createAgent(body):
    email                   = body.get("email")
    password                = body.get("password")
    name                    = body.get("name", "")
    primary_image           = body.get("primary_image","")
    background_image        = body.get("background_image","")
    location                = body.get("location","")
    category                = body.get("category","")
    phone                   = body.get("phone","")
    totalreviews            = body.get("totalreviews",0)
    feedback                = body.get("feedback",0)
    redeemptstoggle = body.get("redeemptstoggle",False)
    starttime               = body.get("starttime")
    starttime = datetime.datetime.strptime(starttime, "%H:%M")
    endtime                 = body.get("endtime")
    endtime = datetime.datetime.strptime(endtime, "%H:%M")
    created_at              = datetime.datetime.now()
    updated_at              = datetime.datetime.now()
    try:
        agent=Agents(email=email, password=password, name=name ,primary_image=primary_image,
                     background_image=background_image, location=location, category=category, phone=phone,redeemptstoggle=redeemptstoggle,
                     starttime=starttime,endtime=endtime,feedback=feedback,totalreviews=totalreviews,created_at=created_at,updated_at=updated_at).save()
        agent=getObjectAsDict(agent._data)
        agent=removeColumnsFromRow(agent)
        return agent
    except Exception as e:
        print e
        return {"error": True}


def getAgentById(id):
    try:
        agent=Agents.objects.get({'_id': ObjectId(id)})
        agent=getObjectAsDict(agent._data)
        agent=removeColumnsFromRow(agent)
        return agent
    except Agents.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}



def getAgentByCredentials(body):
    email      =body.get("email")
    password   =body.get("password")

    try:
        agent=list(Agents.objects.raw({'email': email}))
        agent=getObjectAsDict(agent[0]._data)

        if(agent['password'] == password):
            agent=removeColumnsFromRow(agent)
            agent['token'] = getToken({"id":agent['_id'],"role":"agent"})
            agent['auth-token'] = getToken({"id":login.createLogin(agent['token'],agent['_id'])['_id'],"role":"auth"})
            agent['starttime'] = agent['starttime'].split(" ")[1]
            agent['endtime'] = agent['endtime'].split(" ")[1]
            return agent
        else:
            return {"error": True, "message": "Wrong password"}
    except Exception as e:
        print e, "error"
        return {"error": True, "message": "Wrong email"}


def uploads3( filepath, bucket_name, s3bucket_dir):
    s3.upload_file(filepath, bucket_name,
                   s3bucket_dir,ExtraArgs={'ACL':'public-read'})

    url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': s3bucket_dir, },
    )
    return url.split('?')[0]
def updateAgentBackgroundImg(id, imgcontent):
    agent = Agents.objects.get({"_id": ObjectId(id)})
    imgcontentlist = imgcontent.split('base64,')
    content = imgcontentlist[1].replace(' ', '+').split('\n')[0]
    imgtype = imgcontentlist[0].split('/')[1][:-1]
    missing_padding = len(content) % 4
    if missing_padding != 0:
        content += b'=' * (4 - missing_padding)
        content = base64.b64decode(content)
    else:
        content = base64.b64decode(content)
    with open(id+'.'+imgtype, 'wb') as f:
        f.write(content)
    url = uploads3(id+'.'+imgtype,'pubicbackgroundimages',id+'.'+imgtype)
    os.remove(id+'.'+imgtype)
    agent.background_image = url+"?"+str(datetime.datetime.now().time())
    agent.updated_at = datetime.datetime.now()
    agent.save()
    agent =getObjectAsDict(agent._data)
    agent['starttime'] = agent['starttime'].split(" ")[1]
    agent['endtime'] = agent['endtime'].split(" ")[1]
    return agent
def updateAgent(id, body):
    agent = Agents.objects.get({"_id":ObjectId(id)})
    agent.email = body.get("email",agent.email)
    agent.password = body.get("password",agent.password)
    agent.name = body.get("name", agent.name)
    agent.primary_image = body.get("primary_image", agent.primary_image)
    agent.background_image = body.get("background_image", agent.background_image)
    agent.location = body.get("location", agent.location)
    agent.category = body.get("category", agent.category)
    agent.redeemptstoggle = body.get("redeemptstoggle", agent.redeemptstoggle)
    agent.phone = body.get("phone", agent.phone)
    if body.get("starttime"):
        try:
            agent.starttime = datetime.datetime.strptime(body["starttime"], "%H:%M")
        except:
            agent.starttime = datetime.datetime.strptime(body["starttime"],"%H:%M:%S")
    if body.get("endtime"):
        try:
            agent.endtime = datetime.datetime.strptime(body["endtime"], "%H:%M")
        except:
            agent.endtime = datetime.datetime.strptime(body["endtime"], "%H:%M:%S")

    agent.updated_at = datetime.datetime.now()

    try:
        agent=agent.save()
        agent=getObjectAsDict(agent._data)
        agent['starttime'] = agent['starttime'].split(" ")[1]
        agent['endtime'] = agent['endtime'].split(" ")[1]
        agent=removeColumnsFromRow(agent)
        return agent
    except Agents.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}

def updateFeedback(id, feedback):
    agent = Agents.objects.get({"_id":ObjectId(id)})
    lastfeedback = agent.feedback
    totalreview  = agent.totalreviews
    newfeedback  = float(lastfeedback*totalreview+feedback)/(totalreview+1)
    agent.feedback = newfeedback
    agent.totalreviews = totalreview+1
    agent.updated_at = datetime.datetime.now()

    try:
        agent=agent.save()
        agent=getObjectAsDict(agent._data)
        agent=removeColumnsFromRow(agent)
        return agent
    except Agents.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}


def deleteAgent(id):
    try:
        Agents.delete(Agents(_id=ObjectId(id)))
        return {"success": True}
    except Agents.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}
