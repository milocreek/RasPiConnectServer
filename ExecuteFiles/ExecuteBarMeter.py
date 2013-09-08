#!/usr/bin/python
# Filename: ExecuteBarMeter.py
# Version 2.8 08/12/13 RV MiloCreek

import Config

import subprocess
import xml.etree.ElementTree as ET
import Validate
import BuildResponse

import time


def Execute_BarMeter(root):

      # find the interface object type


        objectServerID = root.find("./OBJECTSERVERID").text
        objectID = root.find("./OBJECTID").text

        if (Config.debug()):
        	print("objectServerID = %s" % objectServerID)

        validate = Validate.checkForValidate(root)

        if (Config.debug()):
        	print "VALIDATE=%s" % validate

        outgoingXMLData = BuildResponse.buildHeader(root)


	# we have the objectServerID so now we can choose the correct
	# program

	# BR-1 sends back the power supply voltage 


	# BR-1
	if (objectServerID == "BR-1"):	


                #check for validate request
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()

                        return outgoingXMLData

		import random
        	if (Config.debug()):
	        	print random.randrange(0,9)
		voltage = 10.0 + (random.randrange(0,9)-10)/10.0
		responseData = "%f" % voltage
                outgoingXMLData += BuildResponse.buildResponse(responseData)
        else:
                # invalid RaspiConnect Code
                outgoingXMLData += Validate.buildValidateResponse("NO")


        outgoingXMLData += BuildResponse.buildFooter()

        return outgoingXMLData




# End of ExecuteBarMeter.py
				
