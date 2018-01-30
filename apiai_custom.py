#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#                                    apiai                                     #
# SDK for api.ai                                                               #
################################################################################

import json
import apiai
import requests
import os


def send (ai, sbuffer, abuffer):
    # Prepares and sends message to apiai the response is returned as-is
    request = ai.text_request()
    request.session_id = sbuffer['sessionId']
    request.query = sbuffer['message']
    # Read the response from apiai
    response = json.loads(request.getresponse().read().decode('UTF-8'))

    abuffer['message']   = response['result']['fulfillment']['speech']
    abuffer['confident'] = response['result']['score']
    abuffer['sessionId'] = response['sessionId']
    abuffer['action']    = response['result']['action']

    return abuffer['action']
