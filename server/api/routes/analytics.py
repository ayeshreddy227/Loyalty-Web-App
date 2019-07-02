from flask import jsonify, request
from api import app
import api.controllers.analytics as analyticsController
from api.libraries.auth_middleware import *

@app.route("/analytics/overviewusers",methods=['GET'])
def overviewinfo():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        agents=analyticsController.newAndReturningUsers(req['id'])
        return jsonify(agents)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/analytics/totalusers",methods=['GET'])
def totalusers():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        agents=analyticsController.totalUsers(req['id'])
        return jsonify(agents)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/analytics/weeklyusers",methods=['GET'])
def weeklyusers():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        agents=analyticsController.totalUserByWeek(req['id'])
        return jsonify(agents)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/analytics/totalrevenue",methods=['GET'])
def totalrevenue():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        agents=analyticsController.totalRevenue(req['id'])
        return jsonify(agents)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/analytics/totaltransactions",methods=['GET'])
def totaltransactions():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        agents=analyticsController.totalRedeemPoints(req['id'])
        return jsonify(agents)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/analytics/weeklytransactions",methods=['GET'])
def weeklytransactions():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        agents=analyticsController.totalTransactionsByWeek(req['id'])
        return jsonify(agents)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/analytics/users",methods=['GET'])
def users():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        agents=analyticsController.totalUsersForMonth(req['id'])
        return jsonify(agents)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/analytics/transactions",methods=['GET'])
def transactions():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        agents=analyticsController.totalRewardsBymonth(req['id'])
        return jsonify(agents)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/analytics/revenue",methods=['GET'])
def revenue():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        agents=analyticsController.revenueBill(req['id'])
        return jsonify(agents)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/analytics/successfulloffer",methods=['GET'])
def successfulloffer():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        agents=analyticsController.successfullOffer(req['id'])
        return jsonify(agents)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})

@app.route("/analytics/userrewardpoints",methods=['GET'])
def userrewardpoints():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers)
    if req["authenticated"] and req["role"] == "agent":
        agents=analyticsController.UsersHoldingRewardPoints(req['id'])
        return jsonify(agents)
    else:
        return jsonify({"error": True, "message": "You are not authorized to access this resource."})
