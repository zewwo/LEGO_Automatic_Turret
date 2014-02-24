''
#######################################################
# Program : 	turret_simple_v1.0
# Description : This program will perform the basic functions of the LEGO Turret.
#				It will shoot, tilt up and down, and rotate.
# History
# ---------------------------------
# Author	Date		Comment
# Kevin		02.22.14	Created, added Key Press inputs for testing
#  ""		02.23.14	Removed Tkinter. Added Threading for Stop Requests (Doesn't work yet)
#######################################################
''

# COMMANDS
# -------------
# u -> aim up
# d -> aim down
# s -> shoot
# r -> rotate


from BrickPi import *
import thread

BrickPiSetup();										# setup motor input

shootMotor = PORT_A									# obtain motor ports and initialize them
BrickPi.MotorEnable[shootMotor] = 1
tiltMotor = PORT_B									
BrickPi.MotorEnable[tiltMotor] = 1

tiltMin = PORT_1									# obtain tilt(touch) sensors and initialize tilt sensors
BrickPi.SensorType[tiltMin] = TYPE_SENSOR_TOUCH
tiltMax = PORT_2
BrickPi.SensorType[tiltMax] = TYPE_SENSOR_TOUCH


BrickPiSetupSensors()								# setup tilt sensors
myinput = ""
flag = False

def stopThread():
	stop = ""
	flag = False
	while BrickPi.Sensor[tiltMax] == 0:
		stop = raw_input("Stop? ")
		
		if stop == "b":
			break	
	
def up():	
	BrickPiUpdateValues()
	
	try:
		thread.start_new_thread(stopThread, () )				# start a thread for user input for stop
	except:
		print "Unable to start Thread"
		
	while BrickPi.Sensor[tiltMax] == 0:				# keep going up until it hits the tilt sensor at max
		BrickPi.MotorSpeed[tiltMotor] = -145
		BrickPiUpdateValues()					
		
	BrickPi.MotorSpeed[tiltMotor] = 0				# turn off the motor
	BrickPiUpdateValues()
	
def down():
	BrickPiUpdateValues()
	
	while BrickPi.Sensor[tiltMin] == 0:				# keep going up until it hits the tilt sensor at max
		BrickPi.MotorSpeed[tiltMotor] = 50
		BrickPiUpdateValues()		
							
	BrickPi.MotorSpeed[tiltMotor] = 0				# turn off the motor
	BrickPiUpdateValues()
			
# function which test the shooting motor
def shoot():
	BrickPi.MotorSpeed[shootMotor] = 255		# turn the motor on to shoot
	BrickPiUpdateValues()

		
while myinput.lower() != "q":
	BrickPi.Timeout = 250
	BrickPiSetTimeout()
	
	myinput = raw_input("Input (Q to quit) : ")

	if  myinput.lower() == "u":			# aim up
		up()
	elif myinput.lower() == "d":		# aim down
		down()
	elif myinput.lower() == "s":		# shoot
		shoot()