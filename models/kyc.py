import json
from flask import Flask, Response, request, jsonify
from flask_restful import Resource, Api
from dotenv import load_dotenv, find_dotenv
import cv2
import datetime
import time
# import requests

import os
load_dotenv(find_dotenv())

app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = r"C:\Users\DELL\Documents\KYC_VERIFICATION"

def upload_image(image):
    print("IMAGE-- ",image.filename)
    image.save(os.path.join(app.config["IMAGE_UPLOADS"]+'\\Uploads\\', image.filename))
    dirname=str(datetime.datetime.now())
    dirname=dirname.replace(':','')
    dirname=dirname.replace('-','')
    dirname=dirname.replace(' ','')
    newpath = r'C:\Documents\KYC_VERIFICATION\\imgdatabase'+str(dirname) +'\\Dataset'
    print(newpath)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    if allowed_pdf(image.filename):
        # formImg(image.filename,dirname)
        print("Hey")     
    else:
        print(image.filename) 
        # formDirectImg(image.filename,dirname)
    return True

def kycUserCreate(request, db):
    print(request.files)
    print(json.loads(request.form["data2"]))
    try:
        data = json.loads(request.form["data2"])
        if request.files:
            image = request.files["document"]
            if(upload_image(image)):
                print("Image uploaded successfully")
            else:
                Exception("Image uploading error")
        else:
            raise Exception("Sorry, no file exist")
        
        query = {
            "fname": data["fname"],
            "lname": data["lname"],
            "email": data["email"],
            "city": data["city"],
            "pincode": data["pincode"],
            "password": data["password"],
            "kycstatus": "False"
        }
        dbresponse = db.user.insert_one(query)
        if(dbresponse):
            return Response(
                response=json.dumps({
                "message":"User created",
                "id":f"{dbresponse.inserted_id}"
            }),
            status = 200,
            mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({
                "message":"User Creation Failed"
            }),
            status = 400,
            mimetype="application/json"
            )
    except Exception as ex:
        print("Exception --- ", ex)
        return Response(
                response=json.dumps({
                "message":"User Creation Failed",
                "error":ex
            }),
            status = 400,
            mimetype="application/json"
            )

    