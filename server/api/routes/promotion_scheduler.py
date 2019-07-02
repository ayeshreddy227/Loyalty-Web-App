from flask import jsonify, request
from api import app
import api.controllers.promotion_scheduler as promotion_schedulersController
from api.libraries.auth_middleware import *


@app.route("/promotion_schedulers",methods=['GET'])
def findPromotionSchedulersByIdForUser():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        promotion_schedulers = promotion_schedulersController.getPromotionsScheduler(req['id'])
        return jsonify(promotion_schedulers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/promotion_schedulers",methods=['POST'])
def createPromotionScheduler():
    content=request.get_json()
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        promotion_schedulers = promotion_schedulersController.createPromotionsScheduler(content,req['id'])
        return jsonify(promotion_schedulers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/promotion_schedulers/<id>",methods=['PUT'])
def updatePromotionScheduler(id):
    content=request.get_json()
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        content["agentId"] = req['id']
        promotion_schedulers = promotion_schedulersController.updatePromotionsScheduler(id, content)
        return jsonify(promotion_schedulers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/promotion_schedulers/<id>",methods=['DELETE'])
def deletePromotionScheduler(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        promotion_schedulers = promotion_schedulersController.deletePromotionsSchedulerScheduler(id)
        return jsonify(promotion_schedulers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})