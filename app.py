from flask import Flask, Response, request
from flask_restful import Resource, Api
from dotenv import load_dotenv, find_dotenv
import os
import pprint
import json
from pymongo import MongoClient
load_dotenv(find_dotenv())
from flask_cors import CORS 
from models.test import *
from models.kyc import *
from models.login import *

app = Flask(__name__)
api=Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# database connectivity
database = os.environ.get("database")

# increased MongoDB timeout
client = MongoClient(database, serverSelectionTimeoutMS=30000)
try:
    if(client):
        print("Connection Established")
    else:
        raise Exception("Database Connection Error")
except Exception as err:
    print(err)

db=client.Hackathon

#API routing

@app.route('/', methods=['GET', 'POST'])
def route1():
    try:
        return "Success"
    except Exception as ex:
        print("Exception --- ", ex)

@app.route('/test', methods=['GET', 'POST'])
def route2():
    try:
        res = function1(request)
        return res
    except Exception as ex:
        print("Exception --- ", ex)

@app.route('/kycUserCreate', methods=['GET', 'POST'])
def route3():
    try:
        res = kycUserCreate(request,db)
        return res
    except Exception as ex:
        print("Exception ---- ", ex)

@app.route('/kycOpenCamera', methods = ['GET', 'POST'])
def route4():
    try:
        res = camera(request, db)
        return res
    except Exception as ex:
        print("Exception ---- ", ex)

@app.route('/login', methods = ['GET', 'POST'])
def route5():
    try:
        res = login(request, db)
        return res
    except Exception as ex:
        print("Exception ---- ", ex)

if __name__ == '__main__':
    app.run(debug=True)
