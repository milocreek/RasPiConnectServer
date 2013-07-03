#!/usr/bin/python
# Filename: config.py
# Version 1.3 04/22/13 JS MiloCreek

# set to True if you wish to see debugging output from the server otherwise False
DEBUG = False 

#WEB_SERVER_PORT is the port that the RasPiConnect Webserver will be responding to requests from the RasPiConnect App
WEB_SERVER_PORT = "9600"

#LOCALURL is the address of your pi. If you poke a hole through your firewall and expose it to the Internet, insert that address here 
#Usually, the port in the URL (9600) will match the WEB_SERVER_PORT above but can be remapped in most routers/firewalls
LOCALURL = "http://192.168.1.120:9600/"

#USERNAME is the username that you have entered in the RasPiConnect App.  It must match and is case sensitive
USERNAME = "RasPiConnect"

#PASSWORD is the password that you have entered in the RasPiConnect App.  It must match and is case sensitive
PASSWORD = "RasPiConnectPassword"

# set to True if you have an I2C bus set up and has an AdaFruit BMP085 and two BlinkM modules (addresses 0xC and 0xB) False if not
I2CDEMO = False 

#RASPICONNECTSERVER Version Number.  Do not change!
VERSIONNUMBER = '2.5'

def localURL():
	return LOCALURL

def password():
	return PASSWORD

def username():
	return USERNAME 

def web_server_port():
	return WEB_SERVER_PORT

def version_number():
	return VERSIONNUMBER

def debug():
	return DEBUG;

def i2c_demo():
	return I2CDEMO;

