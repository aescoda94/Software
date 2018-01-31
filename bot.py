#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#                                  SDKLIB                                      #
# This file contains functions for interfacing other API's and internal tasks  #
################################################################################

import requests
import uuid
import time
import os
import json

def check(JSON, sbuffer,header):
    # Webhook is triggered if a message is sent to the bot. The JSON and the
    # message unciphered are then saved
    # First step is to discard bot's own messages
    print(email)
    if JSON['data']['personEmail'] != os.environ.get('BOT_EMAIL',
                                                                '@sparkbot.io'):
        roomId    = JSON['data']["roomId"]
        print ("Esta es el roomid")
        print(roomId)
        messageId = JSON['data']['id']

        # Message is not in the webhook. GET http request to Spark to obtain it
        message = requests.get(
                        url='https://api.ciscospark.com/v1/messages/'+messageId,
                    headers=header)
        JSON = message.json()
        # Dictionary Containing info would be like this:
        # -------------------
        # |    sessionId    |  Identifies message at API.ai
        # !      roomId     |  Saving just in case
        # |message decrypted|  Used to compare with the message from api.ai
        # |    personId     |  Speaker unique ID
        # |   personEmail   |  Speaker unique email
        # |   displayName   |  Speaker´s displayed name
        # -------------------
        # Different ways of playing with JSON
        messagedecrypt  = JSON.get("text")
        personId        = JSON.get("personId")
        personEmail     = JSON.get("personEmail")
        sessionId = uuid.uuid5(uuid.NAMESPACE_DNS, str(roomId))
        # [Debug]
        #print ("Message Decrypted: "  + messagedecrypt
        #              + "\nroomId: \t"+ roomId
        #            + "\npersonId: \t"+ personId
        #          +"\npersonEmail: \t"+ personEmail
        #          +"\ndisplayName: \t"+ displayName
        #                 +"\nuuid: \t"+ str(sessionId))
        # Save all in buffer for clarification
        sbuffer['sessionId']  = str(sessionId)
        sbuffer['roomId']     = roomId
        sbuffer['message']    = messagedecrypt
        sbuffer['personId']   = personId
        sbuffer['personEmail']= personEmail
        return True
    else:
        print ("message from bot: ignoring")
        return False

def answer(message, roomId,header):
    # This will generate a response to spark
    r = requests.post('https://api.ciscospark.com/v1/messages',
                 headers=header, data=json.dumps({"roomId":roomId,
                                                      "markdown":message
                                                        }))
    return None
