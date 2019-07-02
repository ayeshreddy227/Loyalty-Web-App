from flask import jsonify, request
from api import app
import api.controllers.uploadtos3 as uploadController
from api.libraries.auth_middleware import *

@app.route("/testing",methods=['POST'])
# @cross_origin()
def sdf():
    uploadController.uploadfiletos3(request.content,"sdf.png")