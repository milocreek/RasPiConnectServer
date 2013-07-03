#!/usr/bin/python
# Filename: ExecuteSendText.py
# Version 1.0 04/13/13 JS MiloCreek

import Config

import subprocess
import xml.etree.ElementTree as ET

import Validate
import BuildResponse

import time


def Execute_Send_Text(root):

        # find the interface object type

        objectServerID = root.find("./OBJECTSERVERID").text
        objectFlags = root.find("./OBJECTFLAGS").text
        objectAction = root.find("./OBJECTACTION").text

	if (objectAction == None):
		objectAction = ""

        if (Config.debug()):
		print "OBJECTACTION=%s" % objectAction

        validate = Validate.checkForValidate(root)

        if (Config.debug()):
		print "VALIDATE=%s" % validate

        outgoingXMLData = BuildResponse.buildHeader(root)


        if (Config.debug()):
        	print("objectServerID = %s" % objectServerID)


	# we have the objectServerID so now we can choose the correct
	# program

	# ST-1 writes a file called "ST-1.txt" in the ./local directory with the contents of the text field on RasPiConnect

	if (objectServerID == "ST-1"):	

                #check for validate request
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()

                        return outgoingXMLData
	
		
		responseData = "OK"

		f = open("./local/ST-1.txt", "w")
		f.write( objectAction)      
		f.close()

                outgoingXMLData += BuildResponse.buildResponse(responseData)



        else:
                # invalid RaspiConnect Code
                outgoingXMLData += Validate.buildValidateResponse("NO")



        outgoingXMLData += BuildResponse.buildFooter()
        if (Config.debug()):
        	print outgoingXMLData

	return outgoingXMLData





# End of ExecuteActionButton.py
				
