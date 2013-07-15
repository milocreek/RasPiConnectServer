#!/usr/bin/python
# Filename: ExecuteActionButton.py
# Version 2.5 07/03/13 RV MiloCreek
import Config

import subprocess
import xml.etree.ElementTree as ET

import Validate
import BuildResponse

import time



def Execute_Action_Button(root):

	# conditionally import BlinkM
	if (Config.i2c_demo()):
		from pyblinkm import BlinkM, Scripts
        
	
	
	# find the interface object type

        objectServerID = root.find("./OBJECTSERVERID").text
        objectName = root.find("./OBJECTNAME").text
        objectFlags = root.find("./OBJECTFLAGS").text

        validate = Validate.checkForValidate(root)

        if (Config.debug()):
		print "VALIDATE=%s" % validate

        outgoingXMLData = BuildResponse.buildHeader(root)


        if (Config.debug()):
        	print("objectServerID = %s" % objectServerID)


	# we have the objectServerID so now we can choose the correct
	# program

	# FB-1 just does a toggle from on to off from the button name 

	if (objectServerID == "FB-1"):	
		# do a toggle

                #check for validate request
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()

                        return outgoingXMLData


		responseData = "XXX"

		lowername = objectName.lower()

		if (lowername.count(" off") > 0):
			
			lowername = lowername.replace(" off", " on")
			responseData = lowername.title()
		
		elif (lowername.count(" on") > 0):
			
			lowername = lowername.replace(" on", " off")
			responseData = lowername.title()
			
		else: 
			responseData = objectName
			
                outgoingXMLData += BuildResponse.buildResponse(responseData)



	# B-1 does a toggle on a BlinkM module on I2C bus address 0xb (11)

	elif (objectServerID == "B-1"):	
		# do a toggle

                #check for validate request
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()

                        return outgoingXMLData

		if (Config.debug()):
			print "Config.i2c_demo=%i" % Config.i2c_demo()


		if (Config.i2c_demo()):

			blinkm = BlinkM(1,0xb)
			blinkm.reset()

        		try:
                		blinkm.go_to(0, 0, 255)
				time.sleep(0.2)
                		blinkm.go_to(0, 255, 0)
				responseData = "OK"

        		except IOError as e:
                		#blinkm.reset()
                		print "I/O error({0}): {1}".format(e.errno, e.strerror)
				responseData = "FAILED"
        		except:
                		blinkm.reset()
                		print "Unexpected error:", sys.exc_info()[0]
                		raise

		responseData = "OK"

                outgoingXMLData += BuildResponse.buildResponse(responseData)



        else:
                # invalid RaspiConnect Code
                outgoingXMLData += Validate.buildValidateResponse("NO")



        outgoingXMLData += BuildResponse.buildFooter()
        if (Config.debug()):
        	print outgoingXMLData

	return outgoingXMLData





# End of ExecuteActionButton.py
				
