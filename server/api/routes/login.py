from flask import jsonify, request
from api import app
import api.controllers.login as loginController
from api.libraries.auth_middleware import *

@app.route("/logout",methods=['DELETE'])
def logout():
    auth = auth_validation(request.headers)
    if "error" in auth:
        return jsonify(auth), 401
    req = validate(request.headers,True)
    if req["authenticated"]:
        authtoken = jwt_lib.getPayload(request.headers['auth-token'])["id"]
        admin = loginController.deleteLogin(authtoken)
        return jsonify(admin)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})


@app.route("/sendotp",methods=['GET'])
def sendopt():
    req = validate(request.headers)
    if req["authenticated"]:
        phone = request.headers.get("phone")
        admin = loginController.sendOTP(phone)
        return jsonify(admin)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})

@app.route("/validateotp",methods=['GET'])
def validateotp():
    req = validate(request.headers)
    if req["authenticated"]:
        phone = request.headers.get("phone")
        otp = request.headers.get("otp")
        admin = loginController.validateOTP(phone,otp)
        return jsonify(admin)
    else:
        return jsonify({"error":True,"message":"You are not authorized to access this resource."})
