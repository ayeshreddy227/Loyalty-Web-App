from flask import jsonify, request
from api import app
import api.controllers.consumers as consumerController
import api.controllers.transactions as transactionsController
from api.libraries.auth_middleware import *

@app.route("/consumer",methods=['GET'])
def findAllConsumers():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "admin":
        consumers=consumerController.getAllConsumers()
        return jsonify(consumers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})



@app.route("/consumer/transactions",methods=['GET'])
def recentTransactions():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    headers = request.headers
    if req["authenticated"] and req["role"] == "consumer":
        consumers=transactionsController.getRecentTransactions(req['id'],int(headers['skip']),int(headers['limit']))
        return jsonify(consumers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/consumer",methods=['POST'])
def createConsumer():
    req = validate(request.headers)
    if req["authenticated"]:
        content=request.get_json()
        consumer = consumerController.createConsumer(content)
        return jsonify(consumer)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/consumers/agent/<agentId>",methods=['GET'])
def getConsumersForDashboard(agentId):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        consumers=consumerController.getConsumerByAgentId(agentId)
        return jsonify(consumers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/login/consumer",methods=['POST'])
def ConsumerLogin():
    req = validate(request.headers)
    if req["authenticated"]:
        content=request.get_json()
        consumer = consumerController.loginConsumer(content,content["type"])
        return jsonify(consumer)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/consumer/phone/<id>",methods=['GET'])
def findConsumerByPhone(id):
    req = validate(request.headers)
    if req["authenticated"]:
        consumer = consumerController.checkphone(id)
        if consumer:
            return jsonify(consumer)
        else:
            return jsonify({"error": True, "message": "You are not authorized to access this resource."})
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/consumer/<id>",methods=['GET'])
def findOneConsumer(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "admin":
        consumer = consumerController.getConsumerById(id)
        return jsonify(consumer)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/consumer/name/<id>",methods=['GET'])
def findConsumerNameByID(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "user":
        consumer = consumerController.getConsumerById(id)
        return jsonify({"consumerName":consumer.get("name","")})
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/consumer",methods=['PUT'])
def updateConsumer():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "consumer":
        content=request.get_json()
        consumer = consumerController.updateConsumer(req["id"], content)
        return jsonify(consumer)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/consumer/",methods=['DELETE'])
def deleteConsumer():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "consumer":
        consumer = consumerController.deleteConsumer(req["id"])
        return jsonify(consumer)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})
