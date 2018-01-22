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
