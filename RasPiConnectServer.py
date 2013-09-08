#!/usr/bin/python
# Filename: RasPiConnectServer.py
# Version 2.9 9/07/13 RV MiloCreek

#set up sub directories 

import sys
sys.path.append('./Adafruit')
sys.path.append('./ExecuteFiles')
sys.path.append('./RasPilib')
sys.path.append('./local')
sys.path.append('./config')

# configuration constants

import Config


# system imports

import hashlib
import web
import xml.etree.ElementTree as ET

# RasPiConnectServer execute command routines

import ExecuteServerStatus 
import ExecuteMeter
import ExecuteBarMeter
import ExecuteRemoteWebView
import ExecuteActionButton 
import ExecuteSingleLED 
import ExecuteFreqModLED 
import ExecuteTextAndTitle 
import ExecuteSendText 
import ExecuteFileDirectory



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

FILE_DIRECTORY_CALL = 8192
FILE_READ_CALL = 16384
FILE_WRITE_CALL = 32768


# end interface constants

render = web.template.render('templates/', cache=False)

urls = (
    '/raspi', 'RasPi',
    '/Raspi', 'RasPi',
    '/RasPi', 'RasPi',
    '/Version', 'Version',
    '/version', 'Version',
    '/(.*)', 'index'
)

app = web.application(urls, globals())


class index:
    def POST(self):

	return "<BR>page not available<BR>"
 
class RasPi:
    def POST(self):
        web.header('Content-Type', 'text/html')
	incomingXML = web.data()
	# check for type of incoming request
	#
	#

	# iterate through all the values and pull all the requests together
	# find the interface object type
	root = ET.fromstring(incomingXML)

	if (Config.debug()): 
		print incomingXML

	# start of building the XML responses sent back to the RasPiConnect App

	outgoingData="<XMLRESPONSES>"

	# Parse the XML

	# a message from the RasPiConnect App can consist of many individual control requests for refresh

	for element in root.findall('XMLCOMMAND'): # Get the items out.
    	# Iterate through the list of items(They are in element objects)

		if (Config.debug()): 
    			print 'XMLCOMMAND:' # Yey print stuff out!
    			print 'USERNAME:', element.find('USERNAME').text
    			print 'PASSWORD:', element.find('PASSWORD').text
    			print 'OBJECTNAME:', element.find('OBJECTNAME').text
    			print 'OBJECTTYPE:', element.find('OBJECTTYPE').text
    			print 'OBJECTSERVERID:', element.find('OBJECTSERVERID').text
    			print 'OBJECTID:', element.find('OBJECTID').text

		# authentication	
		
		username = element.find('USERNAME').text
		password = element.find('PASSWORD').text

		m=hashlib.md5()
		m.update(Config.username())
		MD5username = m.hexdigest()
		MD5username = MD5username.upper() 
	
		m=hashlib.md5()
		m.update(Config.password())
		MD5password = m.hexdigest()
		MD5password = MD5password.upper()

		if (Config.debug()): 
			print MD5username
			print MD5password


		# gather the control object type 
		objectType = element.find("./OBJECTTYPE").text
		objectType = int(objectType)
		
		# gather the RasPiConnect ID
		objectID = element.find("./OBJECTID").text
		objectID = int(objectID)


 
	
		if (Config.debug()):
			print("objectType = %i" % objectType)


		# check for password and username.  If they don't match, then return an error and quit
		
		# password username error message
		if (username != MD5username) or (password != MD5password):
		 	if (Config.debug()):
				print("objectType = %i" % objectType)

			outgoingData +="<XMLCOMMAND><OBJECTTYPE>%i" % objectType
			outgoingData +="</OBJECTTYPE>"
			outgoingData +="<OBJECTID>%i" % objectID
			outgoingData +="</OBJECTID>"
			outgoingData +='<ERROR>Username or Password Mismatch</ERROR></XMLCOMMAND>'

			outgoingData+="</XMLRESPONSES>"

			print outgoingData
       			return outgoingData 
	

		# if Local.py is not found, import default LocalExample.py

		local_present = True
		# Check for user imports
		try:
		    import Local
		except ImportError:
		    local_present = False
		    import LocalExample 
		    
		#
		#
		# call user routines 
		#
		#
		#
		if (local_present == True):
			returnData =  Local.ExecuteUserObjects(objectType, element)
		else:
			returnData =  LocalExample.ExecuteUserObjects(objectType, element)

		if (Config.debug()):
			print "Local user objects returns: %s" % returnData
	
		if (len(returnData) != 0):
			outgoingData += returnData
		#
		#
		# if user objects not found (by zero length string), check for the predefined ones
		#
		#
		#
	
		if (len(returnData) == 0):
			
			# call web objects
			if (objectType == REMOTE_WEBVIEW_UITYPE):
			 	if (Config.debug()):
					print "REMOTE_WEBVIEW_UITYPE found"
				outgoingData += ExecuteRemoteWebView.Generate_Remote_WebView(element, Config.localURL())
			elif (objectType == PICTURE_REMOTE_WEBVIEW_UITYPE):
			 	if (Config.debug()):
					print "PICTURE_REMOTE_WEBVIEW_UITYPE found"
				outgoingData += ExecuteRemoteWebView.Generate_Remote_WebView(element, Config.localURL())
	
			# call button objects
			elif (objectType == ACTION_BUTTON_UITYPE): 
			 	if (Config.debug()):
					print "ACTION_BUTTON_UITYPE found"
				outgoingData += ExecuteActionButton.Execute_Action_Button(element)
	
			# call button objects
			elif (objectType == FEEDBACK_ACTION_BUTTON_UITYPE): 
			 	if (Config.debug()):
					print "FEEDBACK_ACTION_BUTTON_UITYPE found"
				outgoingData += ExecuteActionButton.Execute_Action_Button(element)
	
			# call send text objects
			elif (objectType == SEND_TEXT_UITYPE): 
			 	if (Config.debug()):
					print "SEND_TEXT_UITYPE found"
				outgoingData += ExecuteSendText.Execute_Send_Text(element)
	
			# call text and display type 
			elif (objectType == TEXT_DISPLAY_UITYPE): 
			 	if (Config.debug()):
					print "TEXT_DISPLAY_UITYPE found"
				outgoingData += ExecuteTextAndTitle.Execute_Text_And_Title(element)
	
			# call Frequency Modulated LED 
			elif (objectType == FM_BLINK_LED_UITYPE): 
			 	if (Config.debug()):
					print "FM_BLINK_LED_UITYPE found"
				outgoingData += ExecuteFreqModLED.Execute_Freq_Mod_LED(element)
	
			# call single LED objects
			elif (objectType == SINGLE_LED_DISPLAY_UITYPE): 
			 	if (Config.debug()):
					print "SINGLE_LED_DISPLAY_UITYPE found"
				outgoingData += ExecuteSingleLED.Execute_Single_LED(element)
		
			# call speedometer objects 
			elif (objectType == SPEEDOMETER_UITYPE): 
			 	if (Config.debug()):
					print "SPEEDOMETER_UITYPE found"
				outgoingData += ExecuteMeter.Execute_Meter(element)
	
			# call voltmeter objects 
			elif (objectType == VOLTMETER_UITYPE): 
			 	if (Config.debug()):
					print "VOLTMETER_UITYPE found"
				outgoingData += ExecuteMeter.Execute_Meter(element)
	
			# call barmeter objects 
			elif (objectType == BARMETER_UITYPE): 
			 	if (Config.debug()):
					print "BARMETER_UITYPE found"
				outgoingData += ExecuteBarMeter.Execute_BarMeter(element)
	
			# call server objects 
			elif (objectType == SERVER_STATUS_UITYPE): 
			 	if (Config.debug()):
					print "SERVER_STATUS_UITYPE found"
				outgoingData += ExecuteServerStatus.Execute_Server_Status(element)
			# call file directory object 
			elif (objectType == FILE_DIRECTORY_CALL): 
			 	if (Config.debug()):
					print "FILE_DIRECTORY_CALL found"
				outgoingData += ExecuteFileDirectory.Execute_File_Directory(element)
	
			# call file read object 
			elif (objectType == FILE_READ_CALL): 
			 	if (Config.debug()):
					print "FILE_READ_CALL found"
				outgoingData += ExecuteFileDirectory.Execute_File_Read(element)
	
			# call file write object 
			elif (objectType == FILE_WRITE_CALL): 
			 	if (Config.debug()):
					print "FILE_WRITE_CALL found"
				outgoingData += ExecuteFileDirectory.Execute_File_Write(element)
	
			else:
	
				# default error message
			 	if (Config.debug()):
					print("objectType = %i" % objectType)
	
				outgoingData +="<XMLCOMMAND><OBJECTTYPE>%i" % objectType
				outgoingData +="</OBJECTTYPE>"
				outgoingData +="<OBJECTID>%i" % objectID
				outgoingData +="</OBJECTID>"
				outgoingData +='<ERROR>RasPi ObjectType Not Supported</ERROR></XMLCOMMAND>'
	
	# done with FOR loop
	outgoingData+="</XMLRESPONSES>"
	
	if (Config.debug()):
		print "final outgoing data =%s" % outgoingData
       	return outgoingData 
	
class Version:
    def GET(self):
        web.header('Content-Type', 'text/html')
	outGoingData = "<B>RasPiConnectServer Version %s </B><BR>" % Config.version_number() 
        return outGoingData 

web.webapi.internalerror = web.debugerror
if __name__ == '__main__': 
	sys.argv.append(Config.web_server_port())
	app.run()

