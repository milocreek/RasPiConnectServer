#!/usr/bin/python
# Filename: LocalExample.py
# MiloCreek JS MiloCreek
# Version 2.8 8/12/13
#
# Local Execute Objects for RasPiConnect  
# to add Execute objects, modify this file 
#
#
#
# RasPiConnectServer interface constants

REMOTE_WEBVIEW_UITYPE = 1
ACTION_BUTTON_UITYPE = 16
FEEDBACK_ACTION_BUTTON_UITYPE = 17
SINGLE_LED_DISPLAY_UITYPE = 32
SPEEDOMETER_UITYPE = 64
VOLTMETER_UITYPE = 128
BARMETER_UITYPE = 129
SERVER_STATUS_UITYPE = 256
PICTURE_REMOTE_WEBVIEW_UITYPE = 512
LABEL_UITYPE = 1024
FM_BLINK_LED_UITYPE = 2048
TEXT_DISPLAY_UITYPE = 4096
TOGGLE_SWITCH_UITYPE = 33
SEND_TEXT_UITYPE = 34

# system imports
import sys
import subprocess

# RasPiConnectImports

import Config
import Validate
import BuildResponse 

def ExecuteUserObjects(objectType, element):

	# Example Objects

	# fetch information from XML for use in user elements

	#objectServerID is the RasPiConnect ID from the RasPiConnect App

        objectServerID = element.find("./OBJECTSERVERID").text
        objectID = element.find("./OBJECTID").text

        if (Config.debug()):
        	print("objectServerID = %s" % objectServerID)
	# 
	# check to see if this is a Validate request
	#
        validate = Validate.checkForValidate(element)

        if (Config.debug()):
        	print "VALIDATE=%s" % validate

        
	# Build the header for the response

	outgoingXMLData = BuildResponse.buildHeader(element)


	# objects are split up by object types by Interface Constants
	#
	#
	#
	# search for matches to object Type 

	# object Type match
	if (objectType == ACTION_BUTTON_UITYPE):

		if (Config.debug()):
			print "ACTION_BUTTON_UTYPE of %s found" % objectServerID

		# B-2 - play a beep on the Raspberry Pi
		if (objectServerID == "B-2"):	

                	#check for validate request
			# validate allows RasPiConnect to verify this object is here 
                	if (validate == "YES"):
                        	outgoingXMLData += Validate.buildValidateResponse("YES")
                        	outgoingXMLData += BuildResponse.buildFooter()
                        	return outgoingXMLData

			# not validate request, so execute

			# note that python is in the main directory for this call, not the local directory

			output = subprocess.call(["aplay", "sounds/match1.wav"])
			
			responseData = "OK"
                	outgoingXMLData += BuildResponse.buildResponse(responseData)
      			outgoingXMLData += BuildResponse.buildFooter()
                	return outgoingXMLData
		


	else:
		return ""
	# returning a zero length string tells the server that you have not matched 
	# the object and server 
	return ""

