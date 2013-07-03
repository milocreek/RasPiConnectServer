#!/usr/bin/python
# Filename: ExecuteWebView.py
# Version 2.1 04/13/13 RV MiloCreek

import Config

import subprocess
import sys

from Adafruit_BMP085 import * 
import time
import Validate
import BuildResponse

def Generate_Remote_WebView(root, LOCALURL):

       	if (Config.i2c_demo()):
		from pyblinkm import BlinkM, Scripts

	
	objectServerID = root.find("./OBJECTSERVERID").text
        objectFlags = root.find("./OBJECTFLAGS").text
	
	validate = Validate.checkForValidate(root) 

        if (Config.debug()):
		print "VALIDATE=%s" % validate

	outgoingXMLData = BuildResponse.buildHeader(root)

	if (objectServerID == "W-1"):
	
		#check for validate request
		if (validate == "YES"):
			outgoingXMLData += Validate.buildValidateResponse("YES")
			outgoingXMLData += BuildResponse.buildFooter()

			return outgoingXMLData
			
		# normal response requested	
	
		responseData = ""

		# check to see if i2c_demo is turned on
		if (Config.i2c_demo()):
		
        		if (Config.debug()):
				print "Config.i2c_demo passed as True" 


			# Yes, it is on

			# Initialise the BMP085 and use STANDARD mode (default value)
			# bmp = BMP085(0x77, debug=True)
			# bmp = BMP085(0x77)
		
			# To specify a different operating mode, uncomment one of the following:
			# bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
			# bmp = BMP085(0x77, 1)  # STANDARD Mode
			# bmp = BMP085(0x77, 2)  # HIRES Mode
			bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode
			
			count = 0
			exceptionCount = 0
			exceptionCountBMP = 0
			blinkm = BlinkM(1,0xc)
			blinkm.reset()
			
	
			
			try:
				temp = bmp.readTemperature()
				pressure = bmp.readPressure()
				altitude = bmp.readAltitude()
		
				tempData = "%.2f C" % temp
				pressureData = "%.2f hPa" % (pressure / 100.0)

			except IOError as e:
    				exceptionCountBMP = exceptionCountBMP + 1	
				print "I/O error({0}): {1}".format(e.errno, e.strerror)
			except:
    				exceptionCountBMP = exceptionCountBMP + 1	
    				print "Unexpected error:", sys.exc_info()[0]
    				raise

		else:    # now set some values for display since we don't have i2C
			tempData = "xx.x C (no i2c enabled)" 
			pressureData = "xxxx.x hPa (no i2c enabled)" 

				

		# read an HTML template into aw string		
		with open ("./Templates/W-1.html", "r") as myfile:
    			responseData += myfile.read().replace('\n', '')
	
		# replace the URL so it will point to static
		responseData = responseData.replace("XXX", LOCALURL) 
	

		# now replace the AAA, BBB, etc with the right data
		responseData = responseData.replace("AAA", subprocess.check_output(["date", ""], shell=True))	

		# split uptime at first blank, then at first ,
		uptimeString = subprocess.check_output(["uptime", ""])	
	
		uptimeType = uptimeString.split(",")
		uptimeCount = len(uptimeType)

		if (uptimeCount == 6):
			# over 24 hours
			uptimeSplit = uptimeString.split(",")
			uptimeSplit = uptimeSplit[0]+uptimeSplit[1]
			uptimeSplit = uptimeSplit.split(" ", 1)
			uptimeData = uptimeSplit[1]
		else:	
			# under 24 hours
			uptimeSplit = uptimeString.split(" ", 2)
			uptimeSplit = uptimeSplit[2].split(",", 1)
			uptimeData = uptimeSplit[0]

		responseData = responseData.replace("BBB", uptimeData)	

		usersString = subprocess.check_output(["who", "-q"], shell=False, stderr=subprocess.STDOUT,)	
		responseData = responseData.replace("CCC", usersString)	

		freeString = subprocess.check_output(["free", "-mh"])	
		freeSplit = freeString.split("cache: ", 1)
		freeSplit = freeSplit[1].split("       ", 2)
		freeSplit = freeSplit[2].split("\nSwap:", 1)
		freeData = freeSplit[0]


		responseData = responseData.replace("DDD", freeData)	
			
		responseData = responseData.replace("EEE", tempData)	
		responseData = responseData.replace("FFF", pressureData)	


		output = subprocess.check_output(["cat", "/sys/class/thermal/thermal_zone0/temp"])
		cpuTemp = "%3.2f C" % (float(output)/1000.0)
			
		responseData = responseData.replace("GGG", cpuTemp)	
		
		freeString = subprocess.check_output(["ifconfig", "eth0"])	
		freeSplit = freeString.split("inet addr:", 1)
		freeSplit = freeSplit[1].split(" ", 1)
		freeData = freeSplit[0]

		responseData = responseData.replace("HHH", freeData)	
			
		responseData = responseData.replace("III", Config.localURL())
		# responseData = responseData.replace("III", "'your external address here'")

		responseData = responseData.replace("JJJ", Config.version_number())

		# read latest data from ST-1 SendText control on RasPiConnect 

		try:
			with open ("./local/ST-1.txt", "r") as myfile:
    				sendTextData = myfile.read().replace('\n', '')
   		except IOError:
			sendTextData = ""

		responseData = responseData.replace("KKK", sendTextData)

	

		# check to see if i2c_demo is turned on
		if (Config.i2c_demo()):
		
			time.sleep(0.2)

   	 		try:
	
               			blinkm.go_to(255, 0, 0)
				time.sleep(0.2)
               			blinkm.go_to(0, 255, 0)
	
	
       			except IOError as e:
             			#blinkm.reset()
                		exceptionCount = exceptionCount + 1
                		print "I/O error({0}): {1}".format(e.errno, e.strerror)
        		except:
               			blinkm.reset()
                		exceptionCount = exceptionCount + 1
                		print "Unexpected error:", sys.exc_info()[0]
                		raise
	
		#responseData += subprocess.check_output(["cat", "/proc/cpuinfo"])
		#responseData += subprocess.check_output(["cat", "/proc/meminfo"])
		
		outgoingXMLData += BuildResponse.buildResponse(responseData)

        	if (Config.debug()):
			print outgoingXMLData	
	elif (objectServerID == "W-2"):
	
		#check for validate request
		if (validate == "YES"):
			outgoingXMLData += Validate.buildValidateResponse("YES")
			outgoingXMLData += BuildResponse.buildFooter()

			return outgoingXMLData
			
		# normal response requested	

		imageName = "RovioImage.jpg"	


		responseData = "<html><head>"
		responseData += "<title></title><style>body,html,iframe{margin:0;padding:0;}</style>"
		responseData += "</head>"
		
		responseData += "<body><img src=\""
 		responseData += LOCALURL 
 		responseData += "static/"
		responseData += imageName
		responseData += "\" type=\"jpg\" width=\"300\" height=\"300\">"
		responseData += "<BR>Picture<BR>"

		responseData +="</body>"
		
		responseData += "</html>"
	
		
		outgoingXMLData += BuildResponse.buildResponse(responseData)

        	if (Config.debug()):
			print outgoingXMLData	

	else:
		# invalid RaspiConnect Code
		outgoingXMLData += Validate.buildValidateResponse("NO")	
	

	outgoingXMLData += BuildResponse.buildFooter()

	return outgoingXMLData
	

# End of ExecuteWebView.py
				
