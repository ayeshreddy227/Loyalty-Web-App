from flask import jsonify, request
from api import app
import api.controllers.promotions as promotionsController
import api.controllers.user as userController
from api.libraries.auth_middleware import *


@app.route("/promotions",methods=['GET'])
def findAllPromotions():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth),401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        if "present" in request.headers:
            promotions = promotionsController.getPresentPromotionsPerAgent(req["id"])
            return jsonify(promotions)
        else:
            promotions = promotionsController.getAllPromotionsPerAgent(req["id"])
            return jsonify(promotions)
    elif req["authenticated"] and req["role"] == "user":
        agentId = userController.getUserById(req['id'])['agentId']
        promotions = promotionsController.getPresentPromotionsPerAgent(agentId)
        return jsonify(promotions)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/promotions/<id>",methods=['GET'])
def findAllPromotionsForConsumer(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "consumer":
        promotions = promotionsController.getPresentPromotionsPerAgent(req['id'])
        return jsonify(promotions)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/promotion/<id>",methods=['GET'])
def findPromotionsByIdForUser(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "user":
        agentId = userController.getUserById(req['id'])['agentId']
        promotions = promotionsController.getPromotionByIdForUser(id,agentId)
        return jsonify(promotions)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/push/promotions",methods=['GET'])
def pushPromotion():
    headers = request.headers
    if headers['api-key'] == "UmnEFyNbUvqP00eZJGXK":
        promotions = promotionsController.pushPromotions()
        return jsonify(promotions)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/push/scheduler",methods=['GET'])
def pushScheduledPromotion():
    headers = request.headers
    if headers['api-key'] == "UmnEFyNbUvqP00eZJGXK":
        promotions = promotionsController.pushSchedulerRemainder()
        return jsonify(promotions)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/push/birthdaypromotions",methods=['GET'])
def pushBirthdayPromotion():
    headers = request.headers
    if headers['api-key'] == "UmnEFyNbUvqP00eZJGXK":
        promotions = promotionsController.pushBirthdayPromotions()
        return jsonify(promotions)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/promotions",methods=['POST'])
def createPromotion():
    content=request.get_json()
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        promotions = promotionsController.createPromotions(content,req['id'])
        return jsonify(promotions)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/promotions/<id>",methods=['PUT'])
def updatePromotion(id):
    content=request.get_json()
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        content["agentId"] = req['id']
        promotions = promotionsController.updatePromotions(id, content)
        return jsonify(promotions)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/promotions/<id>",methods=['DELETE'])
def deletePromotion(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        promotions = promotionsController.deletePromotions(id)
        return jsonify(promotions)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})