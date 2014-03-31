
''
#######################################################
# Program : PIR Test
# Description : This script will test the PIR Sensor in sensing human movement. 
# History
# ---------------------------------
# Author	Date		Comment
# Kevin		03.11.14	Created.
#######################################################
''

import sys
import select
import tty
import termios

import time
import RPi.GPIO as io

io.setmode(io.BCM)				# set the mode for the GPIO

pir_pin = 18					# the pin where the PIR sensor's YELLOW wire is located at

io.setup(pir_pin, io.IN)			# setup the pir sensor


input = ""

##while input.lower() != "b":
##	print "\nInput T to test the PIR Sensor!"
##	input = raw_input("Your Input : ")
##	
##	if input.lower() == "t":
##		for x in range(0,20):					# iterate 20 times
##			if io.input(pir_pin):				# output pir sensor data
##				print "Sensing! Notice the BLUE"
##			else:		
##				print "No movement in front of sensor!"
##
##			time.sleep(0.2)
##		print "Going back to menu!"
##
####
#All the stuff I'm working on

Current_State = 0
Previous_State = 0

try:
        print "Waiting for the sensor to stop sensing"

        while io.input(pir_pin) == 1:
                Current_State = 0
        print"Ready"

        while True:
                Current_State = io.input(pir_pin)
                if Current_State==1 and Previous_State==0:
                        print"Motion detected"
                        Previous_State=1
                elif Current_State==0 and Previous_State==1:
                        print"Ready"
                        Previous_State=0
                time.sleep(0.1)

except KeyboardInterrupt:
        print "Quit"
        io.cleanup()
