from api.models.admin import Admin
from api.controllers.login import createLogin
from api.libraries.jwt_lib import *
from api.libraries.utilities import *
import pytz
def getAllAdmin():
    admindata=[]
    for row in Admin.objects.all():
        admin = getObjectAsDict(row._data)
        admin = removeColumnsFromRow(admin)
        admindata.append(admin)
    return admindata


def createAdmin(body):
    email                   = body.get("email")
    password                = body.get("password")
    name                    = body.get("name", "")
    created_at              = datetime.datetime.now()
    updated_at              = datetime.datetime.now()
    try:
        admin=Admin(email=email, password=password, name=name,
                     created_at=created_at,updated_at=updated_at).save()
        admin=getObjectAsDict(admin._data)
        admin=removeColumnsFromRow(admin)
        return admin
    except Exception as e:
        print e
        return {"error": True,"message":"Email already exists"}


def getAdminById(id):
    try:
        admin=Admin.objects.get({'_id': ObjectId(id)})
        admin=getObjectAsDict(admin._data)
        admin=removeColumnsFromRow(admin)
        return admin
    except Admin.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}


def getAdminByCredentials(body):
    email      =body.get("email")
    password   =body.get("password")

    try:
        admin=list(Admin.objects.raw({'email': email}))
        admin=getObjectAsDict(admin[0]._data)

        if(admin['password'] == password):
            admin=removeColumnsFromRow(admin)
            admin['token'] = getToken({"id":admin['_id'],"role":"admin"})
            admin['auth-token'] = getToken({"id":createLogin(admin['token'],admin['_id'])['_id'],"role":"auth"})
            return admin
        else:
            return {"error": True, "message": "Wrong password"}
    except Exception as e:
        print e, "error"
        return {"error": True, "message": "Wrong email"}


def updateAdmin(id, body):
    admin = Admin.objects.get({"_id":ObjectId(id)})
    admin.email = body.get("email",admin.email)
    admin.password = body.get("password",admin.email)
    admin.name = body.get("name", admin.email)
    admin.updated_at = datetime.datetime.now()

    try:
        admin=admin.save()
        admin=getObjectAsDict(admin._data)
        admin=removeColumnsFromRow(admin)
        return admin
    except Admin.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}


def deleteAdmin(id):
    try:
        Admin.delete(Admin(_id=ObjectId(id)))
        return {"success": True}
    except Admin.DoesNotExist:
        return {"error": True, "message": "ID does not exist"}
