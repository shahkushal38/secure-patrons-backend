import json
from flask import Flask, Response, request

def function1(request):
    print(json.loads(request.data))
    return Response(
      response=json.dumps({
        "message":"Success",
      }),
      status = 200,
      mimetype="application/json"
    )