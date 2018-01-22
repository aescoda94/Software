#test

import smartsheet
import json
import os
import apiai

import sdk
import spark
import apiaiNlp

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

# Instantiation of APIai object.
ai = apiai.ApiAI(os.environ.get('APIAI_ACCESS_TOKEN', None))


# Buffer for capturing messages from Spark
sbuffer = {"sessionId":"","roomId":"","message":"",
           "personId":"","personEmail":"","displayName":""}
# Buffer for capturing messages from api.ai
abuffer = {"sessionId":"","confident":"", "message":"","action":"",
                                "parameters":""}
# Defining user's dict
user    = {"personId":"","personEmail":"","displayName":""}

# Message Received from Spark
@app.route('/webhook', methods=['POST','GET'])
def webhook():
    # Every message from Spark is received here. I will be analyzed and sent to
    # api.ai response will then sent back to Spark
    req = request.get_json(silent=True, force=True)
    res = spark_webhook(req)
    return None

@app.route('/apiai', methods=['POST','GET'])
def apiai():
    # If there is external data to retrieve, APIai will send a WebHook here
    req = request.get_json(silent=True, force=True)
    # [Debug]
    print("[API.ai] There is an action: "+req["result"]["action"])
    res = apiai_webhook(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

