#!/usr/bin/python
# Filename: ExecuteFileDirectory.py
# Version 1.0 04/09/13 JS MiloCreek

import Config
import glob
import os

import xml.etree.ElementTree as ET

import BuildResponse

import time


def Execute_File_Directory(root):

        # find the interface object type

        objectServerID = root.find("./OBJECTSERVERID").text
        objectFlags = root.find("./OBJECTFLAGS").text
        objectName = root.find("./OBJECTNAME").text



        outgoingXMLData = BuildResponse.buildHeader(root)


        if (Config.debug()):
        	print("objectServerID = %s" % objectServerID)


	# we have the objectServerID so now we can choose the correct
	# program


	if (objectServerID == "FDC-1"):	

		print glob.glob("ClientXMLConfigFiles/*.xml")
	 	file_list = glob.glob("ClientXMLConfigFiles/*.xml")
		responseData = ""

		for pathname in file_list:
				
			responseData += "<FILENAME>"
			responseData += os.path.basename(pathname)			
			responseData += "</FILENAME>"
                

		outgoingXMLData += BuildResponse.buildResponse(responseData)


        else:
                # invalid RaspiConnect Code
                outgoingXMLData += Validate.buildValidateResponse("NO")



        outgoingXMLData += BuildResponse.buildFooter()
        if (Config.debug()):
        	print outgoingXMLData

	return outgoingXMLData


def Execute_File_Read(root):

        # find the interface object type

        objectServerID = root.find("./OBJECTSERVERID").text
        objectFlags = root.find("./OBJECTFLAGS").text
        objectName = root.find("./OBJECTNAME").text



        outgoingXMLData = BuildResponse.buildHeader(root)


        if (Config.debug()):
        	print("objectServerID = %s" % objectServerID)


	# we have the objectServerID so now we can choose the correct
	# program


	if (objectServerID == "FRC-1"):	

		responseData = ""

		print os.getcwd()

		with open ("./ClientXMLConfigFiles/"+objectName, "r") as myfile:
    			responseData=myfile.read().replace('\n', '')
				
                

		outgoingXMLData += BuildResponse.buildResponse(responseData)


        else:
                # invalid RaspiConnect Code
                outgoingXMLData += Validate.buildValidateResponse("NO")



        outgoingXMLData += BuildResponse.buildFooter()
        if (Config.debug()):
        	print outgoingXMLData

	return outgoingXMLData


def Execute_File_Write(root):

        # find the interface object type

        objectServerID = root.find("./OBJECTSERVERID").text
        objectFlags = root.find("./OBJECTFLAGS").text
        objectName = root.find("./OBJECTNAME").text
	objectResponseBody = root.find("./OBJECTRESPONSEBODY").text 


        outgoingXMLData = BuildResponse.buildHeader(root)


        if (Config.debug()):
        	print("objectServerID = %s" % objectServerID)

        if (Config.debug()):
        	print("objectResponseBody = %s" % objectResponseBody)


	# we have the objectServerID so now we can choose the correct
	# program


	if (objectServerID == "FWC-1"):	


		
					
                

		myfile = open("./ClientXMLConfigFiles/"+objectName, "w")
		myfile.write(objectResponseBody)
		myfile.close
		responseData = "OK"
		outgoingXMLData += BuildResponse.buildResponse(responseData)

        else:
                # invalid RaspiConnect Code
                outgoingXMLData += Validate.buildValidateResponse("NO")



        outgoingXMLData += BuildResponse.buildFooter()
        if (Config.debug()):
        	print outgoingXMLData

	return outgoingXMLData




# End of ExecuteFiles.py
				
