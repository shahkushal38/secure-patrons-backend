import json
from flask import Flask, Response, request, jsonify
from flask_restful import Resource, Api
from dotenv import load_dotenv, find_dotenv
import cv2
from datetime import datetime, timedelta
import time
import requests
import fitz
import jwt
import re
from deepface import DeepFace

import os
load_dotenv(find_dotenv())

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
def login(request,db):
    print(json.loads(request.data))
    try:
        data = json.loads(request.data)

        query = {"email": data["email"], "password":data["password"]}
        dbresponse = db.user.find_one(query)

        if(dbresponse and dbresponse["kycstatus"]):
            print("dbresponse",dbresponse)
            token = jwt.encode({
                'email': data['email'],
                # don't foget to wrap it in str function, otherwise it won't work [ i struggled with this one! ]
                'expiration': str(datetime.now() + timedelta(seconds=3600))
                },
                app.config['SECRET_KEY'])
            # jsonify({'token': token.decode('utf-8')})
            # print(token)
            return Response(
                response=json.dumps({
                "message":"User Found",
                "email":data["email"],
                "token":token
            }),
            status = 200,
            mimetype="application/json"
            )

        else:
            return Response(
                response=json.dumps({
                "message":"User Login Failed or KYC is unsuccessfully "
            }),
            status = 400,
            mimetype="application/json"
            )
    except Exception as ex:
        print("Exception --- ", ex)
        return Response(
                response=json.dumps({
                "message":"Login Failed",
                "error":ex
            }),
            status = 400,
            mimetype="application/json"
            )


