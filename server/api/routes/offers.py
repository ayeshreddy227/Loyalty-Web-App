from flask import jsonify, request
from api import app
import api.controllers.offers as offersController
import api.controllers.user as userController
from api.libraries.auth_middleware import *

@app.route("/testing",methods=['POST'])
# @cross_origin()
def sdf():
    # request.headers["Access-Control-Allow-Origin"] = '*'
    # request.headers["Access-Control-Allow-Headers"] = '*'
    sdfsdf = request.get_json()
    sdf = request.headers["ayeshreddy"]
    return jsonify({"message":"sdfadf"})


@app.route("/offers",methods=['GET'])
def findAllOffers():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth),401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        offer_type = request.headers.get("offer_type","rewardpoints")
        if "present" in request.headers:

            offers = offersController.getPresentOffersPerAgent(req["id"],offer_type)
            return jsonify(offers)
        else:
            offers = offersController.getAllOffersPerAgent(req["id"])
            return jsonify(offers)
    elif req["authenticated"] and req["role"] == "user":
        agentId = userController.getUserById(req['id'])['agentId']
        offers = offersController.getPresentOffersPerAgent(agentId)
        return jsonify(offers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/offers/<id>",methods=['GET'])
def findAllOffersForConsumer(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "consumer":
        rewardpoints = int(request.headers.get("rewardpoints"))
        offers = offersController.getPresentOffersPerAgent(id,consumeragentpoints=rewardpoints)
        return jsonify(offers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/offer/<id>",methods=['GET'])
def findOffersByIdForUser(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "user":
        agentId = userController.getUserById(req['id'])['agentId']
        offers = offersController.getOfferByIdForUser(id,agentId)
        return jsonify(offers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})



@app.route("/offers",methods=['POST'])
def createOffer():
    content=request.get_json()
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        offers = offersController.createOffers(content,req['id'])
        return jsonify(offers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/offers/<id>",methods=['PUT'])
def updateOffer(id):
    content=request.get_json()
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        content["agentId"] = req['id']
        offers = offersController.updateOffers(id, content)
        return jsonify(offers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/offers/<id>",methods=['DELETE'])
def deleteOffer(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        offers = offersController.deleteOffers(id)
        return jsonify(offers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})