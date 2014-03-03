''
#######################################################
# Program : 	turret_simple_v1.4
# Description : This program will perform the basic functions of the LEGO Turret.
#				It will shoot, tilt up and down, and rotate.
# History
# ---------------------------------
# Author	Date		Comment
# Kevin		02.22.14	Created, added Key Press inputs for testing
#  ""		02.23.14	Removed Tkinter. Added Threading for Stop Requests (Doesn't work yet)
#  ""		02.24.14	Changed Speed Move Up from -145 to ~(-170). Removed Threading. Added Proper Key Press Input.
#  ""		02.25.14	Added Key Input for Going Down (If needed) + Named Turn Methods.
#  ""		02.27.14	Added Rotation.
#  ""		03.02.14	Changed Batteries, speed for tilt/rotate motor, more documentation.
#######################################################
''

# COMMANDS
# -------------
# w -> aim up
# s -> aim down
# a -> rotate left
# d -> rotate right
# f -> shoot


from BrickPi import *

import sys
import select
import tty
import termios


BrickPiSetup();															# setup motor input

shootMotor = PORT_B														# obtain motor ports and initialize them
BrickPi.MotorEnable[shootMotor] = 1
tiltMotor = PORT_C									
BrickPi.MotorEnable[tiltMotor] = 1
rotateMotor = PORT_A
BrickPi.MotorEnable[rotateMotor] = 1


tiltMin = PORT_1														# obtain tilt(touch) sensors and initialize tilt sensors
BrickPi.SensorType[tiltMin] = TYPE_SENSOR_TOUCH
tiltMax = PORT_2
BrickPi.SensorType[tiltMax] = TYPE_SENSOR_TOUCH



BrickPiSetupSensors()													# setup tilt sensors
myinput = ""

def isData():
	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])	

	
def up():	
	BrickPiUpdateValues()
	old_setting = termios.tcgetattr(sys.stdin)							# save the old settings

	try:
		tty.setcbreak(sys.stdin.fileno())
	
		while BrickPi.Sensor[tiltMax] == 0:								# keep going up until it hits the tilt sensor at max
			if isData():												# check for key input
				key = sys.stdin.read(1)
				if key == 'b':											# stop if user press b
					break												# if there is a key input, break out of loop
			else:
				BrickPi.MotorSpeed[tiltMotor] = -150	
				BrickPiUpdateValues()	
	finally:
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_setting)	# when done, revert back to old settings

	BrickPi.MotorSpeed[tiltMotor] = 0									# turn off the motor
	BrickPiUpdateValues()
	


def down():
	BrickPiUpdateValues()
	old_setting = termios.tcgetattr(sys.stdin)

	try:
		tty.setcbreak(sys.stdin.fileno())

		while BrickPi.Sensor[tiltMin] == 0:								# keep going up until it hits the tilt sensor at max
			if isData():
				key = sys.stdin.read(1)									# read a key press if there is any=
				if key == 'b':				
					break
			else:
				BrickPi.MotorSpeed[tiltMotor] = 25
				BrickPiUpdateValues()		
	finally:
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_setting)
			
	BrickPi.MotorSpeed[tiltMotor] = 0									# turn off the motor
	BrickPiUpdateValues()
			


def shoot():
	old_setting = termios.tcgetattr(sys.stdin)

	try:
		tty.setcbreak(sys.stdin.fileno())

		while True:
			if isData():
				key = sys.stdin.read(1)
				if key == 'b':
					break
			else:
				BrickPi.MotorSpeed[shootMotor] = 255					# turn the motor on to shoot until key is pressed
				BrickPiUpdateValues()
	finally:
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_setting)

	BrickPi.MotorSpeed[shootMotor] = 0
	BrickPiUpdateValues()


def turnLeft():
	BrickPiUpdateValues()
	old_setting = termios.tcgetattr(sys.stdin)				

	try:
		tty.setcbreak(sys.stdin.fileno())
	
		while True:				
			if isData():												# check for key input
				key = sys.stdin.read(1)
				if key == 'b':											# stop if user press b
					break					
			else:
				BrickPi.MotorSpeed[rotateMotor] = -100
				BrickPiUpdateValues()	
	finally:
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_setting)		

	BrickPi.MotorSpeed[rotateMotor] = 0									# turn off the motor
	BrickPiUpdateValues()

def turnRight():
	BrickPiUpdateValues()
	old_setting = termios.tcgetattr(sys.stdin)				

	try:
		tty.setcbreak(sys.stdin.fileno())
	
		while True:				
			if isData():												# check for key input
				key = sys.stdin.read(1)
				if key == 'b':											# stop if user press b
					break					
			else:
				BrickPi.MotorSpeed[rotateMotor] = 100	
				BrickPiUpdateValues()	
	finally:
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_setting)	

	BrickPi.MotorSpeed[rotateMotor] = 0									# turn off the motor
	BrickPiUpdateValues()

while myinput.lower() != "q":
	myinput = raw_input("Input (Q to quit) : ")

	if  myinput.lower() == "w":											# aim up
		up()
	elif myinput.lower() == "s":										# aim down
		down()
	elif myinput.lower() == "a":										# turn left
		turnLeft()	
	elif myinput.lower() == "d":										# turn right
		turnRight()
	elif myinput.lower() == "f":										# shoot
		shoot()

