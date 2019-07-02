from flask import jsonify, request
from api import app
import api.controllers.admin as adminController
from api.libraries.auth_middleware import *
from flask import Flask,send_file

@app.route('/')
def showMachineList():
    try:
        return send_file('static/src/index.html')
    except Exception as e:
        print e

@app.route("/admin",methods=['GET'])
def findAllAdmins():
    req = validate(request.headers,True)
    if req["authenticated"]:
        admin=adminController.getAllAdmin()
        return jsonify(admin)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/admin",methods=['POST'])
def createAdmin():
    req = validate(request.headers,True)
    if req["authenticated"]:
        content=request.get_json()
        admin = adminController.createAdmin(content)
        return jsonify(admin)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/admin/<id>",methods=['GET'])
def findOneAdmin(id):
    req = validate(request.headers,True)
    if req["authenticated"]:
        admin = adminController.getAdminById(id)
        return jsonify(admin)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/login/admin",methods=['POST'])
def AdminLogin():
    req = validate(request.headers,True)
    if req["authenticated"]:
        body = request.get_json()
        admin = adminController.getAdminByCredentials(body)
        return jsonify(admin)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/admin/<id>",methods=['PUT'])
def updateAdmin(id):
    req = validate(request.headers,True)
    if req["authenticated"]:
        content=request.get_json()
        admin = adminController.updateAdmin(id, content)
        return jsonify(admin)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/admin/<id>",methods=['DELETE'])
def deleteAdmin(id):
    req = validate(request.headers,True)
    if req["authenticated"]:
        admin = adminController.deleteAdmin(id)
        return jsonify(admin)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})
