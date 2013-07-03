#!/usr/bin/python
# Filename: ExecuteTextAndTitle.py
# Version 1.5 04/01/13 JS MiloCreek

import Config

import subprocess
import xml.etree.ElementTree as ET

import Validate
import BuildResponse

import time


def Execute_Text_And_Title(root):

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




	if (objectServerID == "LT-1"):	

                #check for validate request
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()

                        return outgoingXMLData

		output = subprocess.check_output(["cat", "/sys/class/thermal/thermal_zone0/temp"])
		FMOutput = float(output)/1000.0




		responseData = "%3.2f, %3.2f, %s" % (FMOutput, FMOutput,"CPU Temp (deg C)")

                outgoingXMLData += BuildResponse.buildResponse(responseData)


	else:

                # invalid RaspiConnect Code
                outgoingXMLData += Validate.buildValidateResponse("NO")


        outgoingXMLData += BuildResponse.buildFooter()
        if (Config.debug()):
        	print outgoingXMLData

        return outgoingXMLData


# End of ExecuteTextAndTitle.py
				
