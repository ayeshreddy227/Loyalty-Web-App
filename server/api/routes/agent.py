from flask import jsonify, request
from api import app
import api.controllers.agents as agentController
import api.controllers.agentaggregation as agentaggregationController
from api.libraries.auth_middleware import *

@app.route("/agent",methods=['GET'])
def findAllAgents():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "admin":
        agents=agentController.getAllAgents()
        return jsonify(agents)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})


@app.route("/agent",methods=['POST'])
def createAgent():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "admin":
        content=request.get_json()
        agent = agentController.createAgent(content)
        return jsonify(agent)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/agent/<id>",methods=['GET'])
def findOneAgent(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "admin":
        agent = agentController.getAgentById(id)
        return jsonify(agent)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/agents/location",methods=["GET"])
def findAgentsByLocation():
    headers = request.headers
    auth = auth_validation(headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(headers)
    if req["authenticated"] and (req["role"] == "consumer" or req['role'] == "agent"):
        agents = agentaggregationController.getAgentByLocation(headers["latitude"],headers['longitude'],headers['skip'],headers['total'],req["id"] if req['role'] == "consumer" else None)
        return jsonify(agents)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})


@app.route("/agents/search",methods=["GET"])
def searchAgentsByLocation():
    headers = request.headers
    auth = auth_validation(headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(headers)
    if req["authenticated"] and (req["role"] == "consumer" or req['role'] == "agent"):
        agents = agentaggregationController.searchAgents(headers["search-str"],headers['skip'],headers['total'],req["id"] if req['role'] == "consumer" else None)
        return jsonify(agents)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})


@app.route("/login/agent",methods=['POST'])
def AgentLogin():
    req = validate(request.headers)
    if req["authenticated"]:
        body = request.get_json()
        agent = agentController.getAgentByCredentials(body)
        return jsonify(agent)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})


@app.route("/agent/<id>",methods=['PUT'])
@app.route("/agent",methods=['PUT'])
def updateAgent(id=None):
    # auth = auth_validation(request.headers)
    # if "error" in auth:
    #     return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and (req["role"] == "admin" or req['role'] == "agent"):
        content=request.get_json()
        if req['role'] == "agent":
            id = req["id"]
            agent = agentController.updateAgent(id, content)
        else:
            agent = agentController.updateAgent(id,content)
        return jsonify(agent)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/backgroundimg/agent",methods=['PUT'])
def updateAgentBackgroundImage(id=None):
    # auth = auth_validation(request.headers)
    # if "error" in auth:
    #     return jsonify(auth), 401

    req = validate(request.headers)
    imgcontent = dict(request.form).values()[0][0].split('\r\n\r')[1].strip()

    if req["authenticated"] and (req["role"] == "admin" or req['role'] == "agent"):
        content=request.form
        if req['role'] == "agent":
            id = req["id"]
            agent = agentController.updateAgentBackgroundImg(id, imgcontent)
        else:
            agent = agentController.updateAgentBackgroundImg(id,imgcontent)
        return jsonify(agent)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})


@app.route("/agent/<id>",methods=['DELETE'])
def deleteAgent(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        agent = agentController.deleteAgent(id)
        return jsonify(agent)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})
