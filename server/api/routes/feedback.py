from flask import jsonify, request
from api import app
import api.controllers.feedback as feedbackController
from api.libraries.auth_middleware import *

@app.route("/feedback",methods=['GET'])
def findAllfeedback():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and (req["role"] == "agent"):
        headers = request.headers
        feedback=feedbackController.getAllFeedbackByAgent(req['id'],int(headers['skip']),int(headers['limit']))
        return jsonify(feedback)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/feedback",methods=['POST'])
def createFeedback():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers,True)
    if req["authenticated"] and req["role"] == "consumer":
        content=request.get_json()
        content['consumerId'] = req["id"]
        feedback = feedbackController.createFeedback(content)
        return jsonify(feedback)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})
@app.route("/feedback/<id>",methods=['PUT'])
def updateFeedback(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers,True)
    if req["authenticated"] and req["role"] == "consumer":
        content=request.get_json()
        content['consumerId'] = req["id"]
        feedback = feedbackController.updateFeedbackData(content,id)
        return jsonify(feedback)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/feedback/<id>",methods=['DELETE'])
def deletefeedback(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers,True)
    if req["authenticated"]:
        admin = feedbackController.deleteFeedback(id)
        return jsonify(admin)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})
