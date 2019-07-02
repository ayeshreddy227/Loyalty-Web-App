from flask import jsonify, request
from api import app
import api.controllers.background_imgs as backgroundimgsController
from api.libraries.auth_middleware import *
from flask import Flask,send_file

@app.route("/backgroundimgs",methods=['GET'])
def findAllBackgroundimgs():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        backgroundimgs=backgroundimgsController.getAllbackgroundimages()
        return jsonify(backgroundimgs)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/backgroundimgs",methods=['POST'])
def createBackgroundimgs():
    req = validate(request.headers,True)
    if req["authenticated"]:
        content=request.get_json()
        backgroundimgs = backgroundimgsController.createBackgroundimages(content)
        return jsonify(backgroundimgs)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/backgroundimgs/<id>",methods=['PUT'])
def updateBackgroundimgs(id):
    req = validate(request.headers,True)
    if req["authenticated"]:
        content=request.get_json()
        backgroundimgs = backgroundimgsController.updateBackgroundimages(id, content)
        return jsonify(backgroundimgs)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/backgroundimgs/<id>",methods=['DELETE'])
def deleteBackgroundimgs(id):
    req = validate(request.headers,True)
    if req["authenticated"]:
        backgroundimgs = backgroundimgsController.deleteBackgroundimages(id)
        return jsonify(backgroundimgs)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})
