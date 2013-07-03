#!/bin/bash 
cd /home/pi/RasPiConnectServer
sudo amixer cset numid=3 1
python RasPiConnectServer.py 
