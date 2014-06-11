#!/usr/bin/python 
# Filename: local.py 
# MiloCreek BP MiloCreek 
# Version 3.0 6/11/2014 
# 
# Local Execute Objects for RasPiConnect  
# to add Execute objects, modify this file 
# 
#
#

# system imports
import sys
import subprocess
import os
import time
# RasPiConnectImports

import Config
import Validate
import BuildResponse 

import RPi.GPIO as GPIO ## Import GPIO library
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT

# To put an LED on GPIO Pin 7 on your pi read this:
#		http://www.thirdeyevis.com/pi-page-2.php
#


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

	#
	# B-1 Flashes LED on GPIO
	if (objectServerID == "B-1"):	

               	#check for validate request
		# validate allows RasPiConnect to verify this object is here 

               	if (validate == "YES"):
                       	outgoingXMLData += Validate.buildValidateResponse("YES")
                       	outgoingXMLData += BuildResponse.buildFooter()
                       	return outgoingXMLData

		# not validate request, so execute
		#
		
		#
		#
		# Execute your code
		#
		#

		# To put an LED on GPIO Pin 7 on your pi read this:
		#		http://www.thirdeyevis.com/pi-page-2.php
		#
        	if (Config.debug()):
        		print("Button # %s: Blinking GPIO pin 7" % objectServerID)

		GPIO.output(7,True) ## Turn on GPIO pin 7
		time.sleep(1) ## sleep 1 second
		GPIO.output(7,False) ## Turn off GPIO pin 7
              	responseData = "OK" ## send an OK back to the App

		print "responseData =", responseData

		#
		#
		# Done with your code
		#
		#

               	outgoingXMLData += BuildResponse.buildResponse(responseData)
      		outgoingXMLData += BuildResponse.buildFooter()
               	return outgoingXMLData
		


	else:
		# returning a zero length string tells the server that you have not matched 
		# the object and server 
		return ""

