from flask import jsonify, request
from api import app
import api.controllers.consumeragent as consumerAgentController
from api.libraries.auth_middleware import *

@app.route("/QRGeneration/<id>",methods=['GET'])
def generateQR(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "consumer":
        consumers=consumerAgentController.generateQRTokenByOffer(id,req["id"])
        return jsonify(consumers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/consumeragent/<id>",methods=['GET'])
def getConsumeragent(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "consumer":
        consumers=consumerAgentController.getConsumerAgentByConsumerAndAgent(id,req["id"])
        return jsonify(consumers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/promotions",methods=['GET'])
def getPromotions():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "consumer":
        consumers=consumerAgentController.getPromotions(req["id"])
        return jsonify(consumers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/validateQR",methods=['GET'])
def validateQR():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and (req["role"] == "agent" or req['role'] == "user"):
        try:
            token = request.headers["qrtoken"]
            bill = request.headers["bill"]
        except:
            return jsonify({"error":True,"message":"missing input params token and bill"})
        consumers=consumerAgentController.validateConsumer(token,bill,req["id"])
        return jsonify(consumers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/dummy",methods=['GET'])
def dummy():
    aa = consumerAgentController.updateConsumerAgent("5ad50c9dae2628123dd6425f",{})
    return jsonify({"a":"a"})

@app.route("/",methods=['GET'])
def base():
    # aa = consumerAgentController.updateConsumerAgent("5ad50c9dae2628123dd6425f",{})
    return jsonify({"a":"a"})

@app.route("/removelistener",methods=['GET'])
def removelistener():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "consumer":
        return jsonify(consumerAgentController.clearFirebase(req['id']))
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})