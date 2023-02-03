import json
from flask import Flask, Response, request

def upload_image():
    dirname=''
    if request.method == "POST":
        if request.files:
            print("REQUEST FILES")
            image = request.files["image"]
            print("IMAGE")
            image.save(os.path.join(app.config["IMAGE_UPLOADS"]+'Uploads\\', image.filename))
            dirname=str(datetime.datetime.now())
            dirname=dirname.replace(':','')
            dirname=dirname.replace('-','')
            dirname=dirname.replace(' ','')
            newpath = r'D:\PROJECT_AND_CODES\KYC_VERIFICATION\\imgdatabase'+str(dirname) +'\\Dataset'
            print(image.filename)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            if allowed_pdf(image.filename):
                formImg(image.filename,dirname)     
            else:
                print(image.filename) 
                formDirectImg(image.filename,dirname)  
    return render_template('stp2.html',dirname=dirname)


def kycUserCreate(request, db):
    print(json.loads(request.data))
    try:
        data = json.loads(request.data)
        if request.files:
            print("Request files")
            image = request.files["image"]
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

    