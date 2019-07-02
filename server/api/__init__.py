from flask import Flask
# # from firebase import firebase
# # firebase = firebase.FirebaseApplication('https://testing-c501c.firebaseio.com', None)
# # result = firebase.get('/users', None)
# # firebase.post('/users',{"name":"ayesh"})
# import pyrebase
#
# config = {
#     "apiKey": "AIzaSyBLpsSXrB2C0-H1OXMD8xpxA46EWWZhAHo",
#     "authDomain": "testing-c501c.firebaseapp.com",
#     "databaseURL": "https://testing-c501c.firebaseio.com",
#     "projectId": "testing-c501c",
#     "storageBucket": "testing-c501c.appspot.com",
#     "messagingSenderId": "159832973877"
#   }
#
# firebase = pyrebase.initialize_app(config)
#
# db = firebase.database()
# # db.child("new")
# data = {"name": "Mortimer"}
# # db.child("new").child("12312312342342").push(data)
# db.child('new').child("12312312342342").remove()
# # print result
# def log_user(response):
#     print "working"
# # while True:
# # firebase.get_async('/users', None, callback=log_user)
# def stream_handler(message):
#     print(message["event"]) # put
#     print(message["path"]) # /-K7yGTTEp7O549EzTYtI
#     print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
#
# my_stream = db.child("new").stream(stream_handler)
app = Flask(__name__)
# app.run(port=5006)
from flask_cors import CORS,cross_origin
cors =CORS(app)