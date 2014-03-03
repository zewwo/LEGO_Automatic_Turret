''
#######################################################
# Program : 	turret_remote_v1.0
# Description : This program will perform the basic functions of the LEGO Turret.
#				It will shoot, tilt up and down, and rotate.
# History
# ---------------------------------
# Author	Date		Comment
# Kevin		02.02.14	Added Wii Remote functionality, reduced motor speeds.
#######################################################
''

# CONTROLS
# -------------
# DPAD UP  	 -> aim up
# DPAD DOWN  -> aim down
# DPAD LEFT  -> rotate left
# DPAD RIGHT -> rotate right
# A B 1 2	 -> shoot

from BrickPi import *

import cwiid
import time

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
	BrickPiUpdateValues()

	if BrickPi.Sensor[tiltMax] == 0 and buttons & cwiid.BTN_UP:									# keep going up until it hits the tilt sensor at max or until the user lets go of the dpad's up button
		BrickPi.MotorSpeed[tiltMotor] = -120
		BrickPiUpdateValues()	
	
	if BrickPi.Sensor[tiltMax] == 1:
		print "Max"
		
	#BrickPi.MotorSpeed[tiltMotor] = 0									# turn off the motor
	BrickPiUpdateValues()
	BrickPi.MotorSpeed[tiltMotor] = 0

def down():
	BrickPiUpdateValues()

	if BrickPi.Sensor[tiltMin] == 0 and buttons & cwiid.BTN_DOWN:								# keep going up until it hits the tilt sensor at max or until the user lets go of the dpad's down button
		BrickPi.MotorSpeed[tiltMotor] = 25
		BrickPiUpdateValues()
			
	if BrickPi.Sensor[tiltMin] == 1:
		print "Min"

	#BrickPi.MotorSpeed[tiltMotor] = 0									# turn off the motor
	BrickPiUpdateValues()
	BrickPi.MotorSpeed[tiltMotor] = 0		

def shoot():
	while True:
		BrickPi.MotorSpeed[shootMotor] = 255					# turn the motor on to shoot until the user lets go of the B, A, 1, or 2 button
		BrickPiUpdateValues()
				
	BrickPi.MotorSpeed[shootMotor] = 0
	BrickPiUpdateValues()


def turnLeft():
	while True:														# turn left until the user lets go of the dpad's left button
		BrickPi.MotorSpeed[rotateMotor] = -80
		BrickPiUpdateValues()	
				
	BrickPi.MotorSpeed[rotateMotor] = 0									# turn off the motor
	BrickPiUpdateValues()

	
def turnRight():
	while True:														# turn left until the user lets go of the dpad's right button
		BrickPi.MotorSpeed[rotateMotor] = 80	
		BrickPiUpdateValues()	

	BrickPi.MotorSpeed[rotateMotor] = 0									# turn off the motor
	BrickPiUpdateValues()

	
	
print "Press 1 + 2 on your Wii Remote to connect to the turret..."
time.sleep(1)

try:
	wii = cwiid.Wiimote()												# attempt to connect the wii remote to the script
except RuntimeError:
	print "Error: Wii Remote cannot be connected..."					# exit the script if the wii remote cannot be connected
	quit()								

wii.rumble = 1															# rumble for two seconds to indicate that it has been connected
time.sleep(2)
wii.rumble = 0
	
print "Wii Remote has been connected! \n"
print "\tControls :"
print "DPAD UP = Aim Up\tDPAD DOWN = Aim Down"
print "DPAD LEFT = Turn Left\tDPAD RIGHT = Turn Right"
print "\t\tA B 1 2 = Shoot"
print "\n Press + and - to exit the script"
	
wii.rpt_mode = cwiid.RPT_BTN											# set the mode to report button presses
	
while True:																# exit code when the user press + and - on the remote	
	buttons = wii.state['buttons']										# get current remote states

	if buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0:					# check if the user pressed + and - simultaneously
		print "Exiting script and connection..."
		wii.rumble = 1													# rumble for 1s to indicate the user that it is exiting the script
		time.sleep(1)
		wii.rumble = 0
		exit(wii)
		quit()									
	
	if buttons & cwiid.BTN_UP:											# perform function calls according to what the state of the wii remote is
		up()
		print "Up"
		time.sleep(delay)
	elif buttons & cwiid.BTN_DOWN:										
		down()
		print "Down"
		time.sleep(delay)
	elif buttons & cwiid.BTN_LEFT:										
		#turnLeft()	
		print "Left"
		time.sleep(delay)
	elif buttons & cwiid.BTN_RIGHT:										
		#turnRight()
		print "Right"
		time.sleep(delay)
	elif buttons & cwiid.BTN_A or buttons & cwiid.BTN_B or buttons & cwiid.BTN_1 or buttons & cwiid.BTN_2:
		#shoot()
		print "Shoot"
		time.sleep(delay)
