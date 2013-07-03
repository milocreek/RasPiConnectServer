#!/usr/bin/python
# Filename: ExecuteMeter.py
# Version 2.2 03/13/13 RV MiloCreek

import Config

import subprocess
import xml.etree.ElementTree as ET
import Validate
import BuildResponse

import time


def Execute_Meter(root):

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

	# M-1 sends back the power supply voltage 
	# M-2 sends back the number of processes running on the Raspberry Pi 


	# M-1
	if (objectServerID == "M-1"):	


                #check for validate request
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()

                        return outgoingXMLData

		import random
        	if (Config.debug()):
	        	print random.randrange(0,9)
		voltage = 5.0 + (random.randrange(0,9)-5)/10.0
		responseData = "%f" % voltage
                outgoingXMLData += BuildResponse.buildResponse(responseData)

	# M-2
	elif (objectServerID == "M-2"):	

                #check for validate request
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()

                        return outgoingXMLData

		p1 = subprocess.Popen(['ps', 'xaf'], stdout=subprocess.PIPE)
		p3 = subprocess.Popen(['wc', '-l'], stdin=p1.stdout,stdout=subprocess.PIPE)
		p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p3 exits.
		output = p3.communicate()[0]
		numberofprocesses = int(output)
		responseData = "%i" % numberofprocesses
                outgoingXMLData += BuildResponse.buildResponse(responseData)
        else:
                # invalid RaspiConnect Code
                outgoingXMLData += Validate.buildValidateResponse("NO")


        outgoingXMLData += BuildResponse.buildFooter()

        return outgoingXMLData




# End of ExecuteMeter.py
				
