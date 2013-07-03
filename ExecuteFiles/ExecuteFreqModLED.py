#!/usr/bin/python
# Filename: ExecuteFreqModLED.py
# Version 1.3 04/01/13 JS MiloCreek

import Config

import subprocess
import xml.etree.ElementTree as ET

import Validate
import BuildResponse

import time


def Execute_Freq_Mod_LED(root):

        # find the interface object type

        objectServerID = root.find("./OBJECTSERVERID").text
        objectFlags = root.find("./OBJECTFLAGS").text

        validate = Validate.checkForValidate(root)

        if (Config.debug()):
        	print "VALIDATE=%s" % validate

        outgoingXMLData = BuildResponse.buildHeader(root)


        if (Config.debug()):
        	print("objectServerID = %s" % objectServerID)

	# we have the objectServerID so now we can choose the correct
	# program

	# L-1 sends back the current second to provide an interesting display 



	if (objectServerID == "BL-1"):	

                #check for validate request
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()

                        return outgoingXMLData

		output = subprocess.check_output(["uptime", ""])
		list = output.split("average:")
		list2 = list[1].split(",")
        	if (Config.debug()):
			print list2
			print list2[0]	
		element = list2[0]

		FMOutput = 1/(float(element)*4.0+0.01)



		responseData = "%3.2f, %3.2f, %s" % (FMOutput, float(element),"CPU Load")


                outgoingXMLData += BuildResponse.buildResponse(responseData)


	else:

                # invalid RaspiConnect Code
                outgoingXMLData += Validate.buildValidateResponse("NO")


        outgoingXMLData += BuildResponse.buildFooter()
        if (Config.debug()):
        	print outgoingXMLData

        return outgoingXMLData


# End of ExecuteFreqModLED.py
				
