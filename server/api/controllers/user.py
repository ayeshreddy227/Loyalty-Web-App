from api.models.user import User
from api.libraries.jwt_lib import *
from api.libraries.utilities import *
import pytz
import login
def getAllUser():
    user=[]
    for row in User.objects.all():
        agent = getObjectAsDict(row._data)
        agent = removeColumnsFromRow(agent)
        user.append(agent)
    return user


def createUser(body,id):
    email                   = body.get("email")
    password                = body.get("password")
    agentId                 = id
    created_at              = datetime.datetime.now()
    updated_at              = datetime.datetime.now()
    try:
        agent=User(email=email, password=password,agentId=agentId,created_at=created_at,updated_at=updated_at).save()
        agent=getObjectAsDict(agent._data)
        agent=removeColumnsFromRow(agent)
        return agent
    except Exception as e:
        print e
        return {"error": True}


def getUserById(id):
    try:
        agent=User.objects.get({'_id': ObjectId(id)})
        agent=getObjectAsDict(agent._data)
        agent=removeColumnsFromRow(agent)
        return agent
    except User.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}



def getUserByCredentials(body):
    email      =body.get("email")
    password   =body.get("password")

    try:
        agent=list(User.objects.raw({'email': email}))
        agent=getObjectAsDict(agent[0]._data)

        if(agent['password'] == password):
            agent=removeColumnsFromRow(agent)
            agent['token'] = getToken({"id":agent['_id'],"role":"user"})
            agent['auth-token'] = getToken({"id":login.createLogin(agent['token'],agent['_id'])['_id'],"role":"auth"})
            return agent
        else:
            return {"error": True, "message": "Wrong password"}
    except Exception as e:
        print e, "error"
        return {"error": True, "message": "Wrong email"}


def updateUser(id, body):
    agent = User.objects.get({"_id":ObjectId(id)})
    agent.email = body.get("email",agent.email)
    agent.password = body.get("password",agent.password)
    agent.updated_at = datetime.datetime.now()

    try:
        agent=agent.save()
        agent=getObjectAsDict(agent._data)
        agent=removeColumnsFromRow(agent)
        return agent
    except User.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}


def deleteUser(id):
    try:
        User.delete(User(_id=ObjectId(id)))
        return {"success": True}
    except User.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}
