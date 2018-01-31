
import json
import os
import apiai
import apic_EM_func
import bot
import apiai_custom
from flask import Flask
from flask import request


# Flask app should start in global layout
app = Flask(__name__)

# Instantiation of APIai object.
ai = apiai.ApiAI(os.environ.get('APIAI_ACCESS', None))

# Instantiation of SPARK token
spark_header = {
        'Authorization': 'Bearer ' + os.environ.get('SPARK_ACCESS', None),
        'Content-Type': 'application/json'
        }

# Buffer for capturing messages from Spark
sbuffer = {"sessionId":"","roomId":"","message":"",
           "personId":"","personEmail":"","displayName":""}
# Buffer for capturing messages from api.ai
abuffer = {"sessionId":"","confident":"", "message":"","action":"",
                                "parameters":""}
# Defining user's dict
user    = {"personId":"","personEmail":"","displayName":""}

# Message Received from Spark
@app.route('/message', methods=['POST','GET'])
def message():
    # Every message from Spark is received here. I will be analyzed and sent to
    # api.ai response will then sent back to Spark
    req = request.get_json(silent=True, force=True)
    res = message_read(req)
    return '200'

def message_read(req):
    # JSON is from Spark. This will contain the message, a personId, displayName,
    # and a personEmail that will be buffered for future use.
    # This time, code has been splitted in different parts for clarity
    # The next function is contained at the sdk file on the same path
    # as this main code.
    if bot.check(req, sbuffer,spark_header):

        action = apiai_custom.send (ai, sbuffer, abuffer)

        if action == 'reach':
                data = get_reachability()
                sbuffer["message"] = data
                return None
        elif action == "ip":
                data = get_hosts()
                sbuffer["message"] = data
                return None
        elif action == "devices":
                data = get_devices()
                sbuffer["message"] = data
                return None
        else:
                status = "apiai does not know the answer"
                sbuffer["message"] = "Ups, apiai no ha asociado su pregunta a \
                ninguna acción"
                return None
        bot.answer(sbuffer["message"],sbuffer['roomId'])
        return None
    else:
        status = "Error buffering or message from bot"
        return None


# App is listening to webhooks. Next line is used to executed code only if it is
# running as a script, and not as a module of another script.
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0', threaded=True)
        
