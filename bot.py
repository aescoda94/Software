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

#Sparkbot email defined as a environment variable
bot_email = os.environ.get('BOT_EMAIL','@sparkbot.io'):

def check(JSON, sbuffer,header):
    # Webhook is triggered if a message is sent to the bot. The JSON and the
    # message unciphered are then saved
    # First step is to discard bot's own messages
    if JSON['data']['personEmail'] != bot_email:
        roomId    = JSON['data']["roomId"]
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
        # The Display Name of the person must be obtained from Spark too.
        # To get the displayName of the user, Spark only needs to know the
        # personId or the personEmail
        displayName = get_displayName(personId)
        # [WARNING] UUIDV1 specifies string + time ID. Maybe there is need to use
        # roomId as identification, but not very well specified in Docs
        #sessionId = uuid.uuid1()
        # Session ID is based on roomId and Heroku URL
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
        sbuffer['displayName']= displayName
        return True
    else:
        print ("message from bot: ignoring")
        return False

def answer(message, roomId):
    # This will generate a response to spark
    r = requests.post('https://api.ciscospark.com/v1/messages',
                 headers=spark_header, data=json.dumps({"roomId":roomId,
                                                      "markdown":message
                                                        }))
    print("Code after send_message POST: "+str(r.status_code))
    status= "Message sent to Spark"
    if r.status_code !=200:
        print(str(json.loads(r.text)))
        if   r.status_code == 403:
            status= "Oops, no soy moderador del team de dicha sala"
        elif r.status_code == 404:
            status= "Disculpe. Ya no soy miembro ni moderador de dicho grupo"
        elif r.status_code == 409:
            status= "Lo siento, no ha podido ser enviado (409)"
        elif r.status_code == 500:
            status= "Perdón, los servidores de Spark están sufriendo problemas.\
                               Compruébelo aquí: https://status.ciscospark.com/"
        elif r.status_code == 503:
            status= "Lo siento. Parece ser que los servidores de Spark no \
                                            pueden recibir mensajes ahora mismo"
        else:
            response = r.json()
            status= str('Error desconocido: \ '
                                         + response['errors'][0]['description'])
    return status

def get_displayName (personId):
    # To get the displayName of the user, Spark only needs to know the personId
    # or the personEmail
    message = requests.get(url='https://api.ciscospark.com/v1/people/'+personId,
                        headers=spark_header)
    JSON = message.json()
    return JSON.get("displayName")