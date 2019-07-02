# from pymongo import MongoClient
# client=MongoClient('localhost:27017')
# db=client["turing"]
import api
from pymodm import connect
# Connect to MongoDB and call the connection "my-app".
# connect("mongodb://localhost:27017/turing")
# connect("mongodb://13.127.94.203:27017/su")
connect("mongodb://localhost:27017/su")
