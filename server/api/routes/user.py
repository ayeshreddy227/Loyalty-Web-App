from flask import jsonify, request
from api import app
import api.controllers.user as userController
import api.controllers.transactions as transactionsController
from api.libraries.auth_middleware import *

@app.route("/user",methods=['GET'])
def findAllUsers():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "user":
        users=userController.getAllUser()
        return jsonify(users)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/user/transactions",methods=['GET'])
def recentTransactionsByAgent():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    headers = request.headers
    if req["authenticated"] and req["role"] == "user":
        agentId = userController.getUserById(req['id'])['agentId']
        consumers=transactionsController.getRecentTransactionsByAgent(agentId,int(headers['skip']),int(headers['limit']))
        return jsonify(consumers)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})



@app.route("/user",methods=['POST'])
def createUser():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        content=request.get_json()
        user = userController.createUser(content,req['id'])
        return jsonify(user)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/user/<id>",methods=['GET'])
def findOneUser(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "user":
        user = userController.getUserById(id)
        return jsonify(user)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/login/user",methods=['POST'])
def UserLogin():
    req = validate(request.headers)
    if req["authenticated"]:
        body = request.get_json()
        user = userController.getUserByCredentials(body)
        return jsonify(user)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})


@app.route("/user/<id>",methods=['PUT'])
@app.route("/user",methods=['PUT'])
def updateUser(id=None):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and (req["role"] == "admin" or req['role'] == "user"):
        content=request.get_json()
        if req['role'] == "user":
            id = req["id"]
            user = userController.updateUser(id, content)
        else:
            user = userController.updateUser(id,content)
        return jsonify(user)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/user/<id>",methods=['DELETE'])
def deleteUser(id):
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "user":
        user = userController.deleteUser(id)
        return jsonify(user)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})
