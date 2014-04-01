''
#######################################################
# Program : 	turret_sensor
# Description : 
# History
# ---------------------------------
# Author	Date		Comment
# Nathan	03.15.14	Created.
#######################################################
''

# CONTROLS ( TURN WII REMOTE HORIZONTALLY )
# -------------
# DPAD UP    -> aim up
# DPAD DOWN  -> aim down
# DPAD LEFT  -> rotate left
# DPAD RIGHT -> rotate right
# 2	     -> shoot ( disabled in auto shoot mode )
# HOME	     -> auto shoot mode ( from remote mode )
# 1          -> remote mode ( from auto shoot )

from BrickPi import *

import cwiid
import time

import sys
import select
import tty
import termios
import RPi.GPIO as io

io.setmode(io.BCM)

pir_pin = 18
io.setup(pir_pin, io.IN)

BrickPiSetup();															# setup motor input

rotateMotor = PORT_A													# obtain motor ports and initialize them
BrickPi.MotorEnable[rotateMotor] = 1
shootMotor = PORT_B														
BrickPi.MotorEnable[shootMotor] = 1
tiltMotor = PORT_C									
BrickPi.MotorEnable[tiltMotor] = 1


tiltMin = PORT_1														# obtain tilt(touch) sensors and initialize tilt sensors
BrickPi.SensorType[tiltMin] = TYPE_SENSOR_TOUCH
tiltMax = PORT_2
BrickPi.SensorType[tiltMax] = TYPE_SENSOR_TOUCH


BrickPiSetupSensors()													# setup tilt sensors
myinput = ""

delay = 0.1
	
def up():	
	if BrickPi.Sensor[tiltMax] == 0 and buttons & cwiid.BTN_RIGHT:				# keep going up until it hits the tilt sensor at max or until the user lets go of the dpad's right button
		BrickPi.MotorSpeed[tiltMotor] = -130
		BrickPiUpdateValues()

	if BrickPi.Sensor[tiltMax] == 0 and senseButs & cwiid.BTN_RIGHT:
		BrickPi.MotorSpeed[tiltMotor] = -130
		BrickPiUpdateValues()

def down():
	if BrickPi.Sensor[tiltMin] == 0 and buttons & cwiid.BTN_LEFT:				# keep going up until it hits the tilt sensor at max or until the user lets go of the dpad's left button
		BrickPi.MotorSpeed[tiltMotor] = 30		
		BrickPiUpdateValues()
	if BrickPi.Sensor[tiltMin] == 0 and senseButs & cwiid.BTN_LEFT:				# keep going up until it hits the tilt sensor at max or until the user lets go of the dpad's left button
		BrickPi.MotorSpeed[tiltMotor] = 30		
		BrickPiUpdateValues()
	

def shoot():
	if buttons == 1:
		BrickPi.MotorSpeed[shootMotor] = 255							# turn the motor on to shoot until the user lets go of the 2 button
		BrickPiUpdateValues()
	elif io.input(pir_pin):
		BrickPi.MotorSpeed[shootMotor] = 255							# turn the motor on to shoot until the user lets go of the 2 button
		BrickPiUpdateValues()


def turnLeft():
	if buttons & cwiid.BTN_UP:													# turn left until the user lets go of the dpad's left button
		BrickPi.MotorSpeed[rotateMotor] = -130
		BrickPiUpdateValues()	
	if senseButs & cwiid.BTN_UP:													# turn left until the user lets go of the dpad's left button
		BrickPi.MotorSpeed[rotateMotor] = -130
		BrickPiUpdateValues()
	
def turnRight():
	if buttons & cwiid.BTN_DOWN:													# turn left until the user lets go of the dpad's right button
		BrickPi.MotorSpeed[rotateMotor] = 130
		BrickPiUpdateValues()	
	if senseButs & cwiid.BTN_DOWN:													# turn left until the user lets go of the dpad's right button
		BrickPi.MotorSpeed[rotateMotor] = 130	
		BrickPiUpdateValues()


print "\nPress 1 + 2 on your Wii Remote to connect to the turret..."
time.sleep(1)

while True:											# keep looping until there is a wii remote connected
	try:
		wii = cwiid.Wiimote()												# attempt to connect the wii remote to the script
		break
	except RuntimeError:
		print "Attempting to find Wii remotes..."					

wii.rumble = 1															# rumble for two seconds to indicate that it has been connected
time.sleep(2)
wii.rumble = 0
wii.led = 1	
print "Wii Remote has been connected! \n"
print "\n\t\tRemote Mode!"
print "Controls ( TURN WII REMOTE HORIZONTALLY ):"
print "DPAD UP = Aim Up\tDPAD DOWN = Aim Down"
print "DPAD LEFT = Turn Left\tDPAD RIGHT = Turn Right"
print "2 = Shoot\t\tHOME = Go to Auto Shoot Mode!"
print "\nPress + and - to exit the script"
	
wii.rpt_mode = cwiid.RPT_BTN											# set the mode to report button presses

while True:																# exit code when the user press + and - on the remote	
	buttons = wii.state['buttons']										# get current remote states
	senseButs = 0

	if buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0:					# check if the user pressed + and - simultaneously
		print "Exiting script and connection..."
		wii.rumble = 1													# rumble for 1s to indicate the user that it is exiting the script
		time.sleep(1)
		wii.rumble = 0
		exit(wii)
		quit()									
	
	if buttons & cwiid.BTN_RIGHT:										# perform function calls according to what the state of the wii remote is
		up()
	elif buttons & cwiid.BTN_LEFT:										
		down()
	elif buttons & cwiid.BTN_UP:										
		turnLeft()	
	elif buttons & cwiid.BTN_DOWN:										
		turnRight()
	elif buttons & cwiid.BTN_2:
		shoot()
	elif buttons & cwiid.BTN_HOME:
		wii.led = 2
		print "\n\n\t\tAuto Shoot Mode!"
		print "(Uses PIR Sensor + Manual Shooting is disabled!)"
		print "\t\tSame Controls"
		print "\t1 = Go back to Remote Mode!"
		while True:
			senseButs = wii.state['buttons']			

			if senseButs & cwiid.BTN_1:						# go back to normal mode if user pressed 1
				wii.rumble = 1
				time.sleep(1)
				wii.rumble = 0
				wii.led = 1
				break
		
			if senseButs & cwiid.BTN_RIGHT:
				up()
			elif senseButs & cwiid.BTN_LEFT:
				down()
			elif senseButs & cwiid.BTN_UP:
				turnLeft()
			elif senseButs & cwiid.BTN_DOWN:
				turnRight()
			if senseButs == 0:
				BrickPi.MotorSpeed[tiltMotor] = 0	
				BrickPi.MotorSpeed[rotateMotor] = 0	
				BrickPiUpdateValues()

			if io.input(pir_pin):							# shoot for 4s if the sensor activates
				shoot()
			else:
				BrickPi.MotorSpeed[shootMotor] = 0
				BrickPiUpdateValues()	
			time.sleep(delay)
		print "\n\t\tRemote Mode!"
		print "Controls ( TURN WII REMOTE HORIZONTALLY ):"
		print "DPAD UP = Aim Up\tDPAD DOWN = Aim Down"
		print "DPAD LEFT = Turn Left\tDPAD RIGHT = Turn Right"
		print "2 = Shoot\t\tHOME = Go to Auto Shoot Mode!"
		print "\nPress + and - to exit the script"
	
	if buttons == 0:													# if there are no buttons that are pressed turn all motors off
		BrickPi.MotorSpeed[shootMotor] = 0
		BrickPi.MotorSpeed[tiltMotor] = 0	
		BrickPi.MotorSpeed[rotateMotor] = 0	
		BrickPiUpdateValues()
	
	time.sleep(delay)
