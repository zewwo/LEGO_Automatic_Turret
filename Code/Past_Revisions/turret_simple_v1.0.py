''
#######################################################
# Program : 	turret_simple_v1.0
# Description : This program will perform the basic functions of the LEGO Turret.
#				It will shoot, tilt up and down, and rotate.
# History
# ---------------------------------
# Author	Date		Comment
# Kevin		02.22.14	Created, added Key Press inputs for testing
#
#######################################################
''

# COMMANDS
# -------------
# u -> aim up
# d -> aim down
# s -> shoot
# r -> rotate


from BrickPi import *
import Tkinter

BrickPiSetup();										# setup motor input

shootMotor = PORT_A									# obtain motor ports and initialize them
BrickPi.MotorEnable[shootMotor] = 1
tiltMotor = PORT_B									
BrickPi.MotorEnable[tiltMotor] = 1

tiltMin = PORT_1									# obtain tilt(touch) sensors and initialize tilt sensors
BrickPi.SensorType[tiltMin] = TYPE_SENSOR_TOUCH
tiltMax = PORT_5
BrickPi.SensorType[tiltMax] = TYPE_SENSOR_TOUCH


BrickPiSetupSensors()								# setup tilt sensors
root = Tkinter.Tk()									# initialize tkinter
ans = ""

def keypress(event):
	key = event.char
	
	if key == "b":									# break the loop if b was pressed
		break
	elif event.keysym == 'Escape':					# ???
		root.destroy()
	# else if turn the motor on, update values

def up():	
	while BrickPi.Sensor[tiltMax] == 0:				# keep going up until it hits the tilt sensor at max
		BrickPi.MotorSpeed[tiltMotor] = -50
		BrickPiUpdateValues()
		
		root.bind_all('<Key>', keypress)			# read a key press to break the loop and go back to main menu
		root.withdraw()
		root.mainloop()								
		
	BrickPi.MotorSpeed[tiltMotor] = 0				# turn off the motor
	BrickPiUpdateValues()
	
def down():
	while BrickPi.Sensor[tiltMin] == 0:				# keep going up until it hits the tilt sensor at max
		BrickPi.MotorSpeed[tiltMotor] = 50
		BrickPiUpdateValues()		
		
		root.bind_all('<Key>', keypress)			# read a key press to break the loop and go back to main menu
		root.withdraw()
		root.mainloop()								
		
	BrickPi.MotorSpeed[tiltMotor] = 0				# turn off the motor
	BrickPiUpdateValues()
			
# function which test the shooting motor
def shoot():
	while True:	
		# set the brick pi to stop at 150ms
		BrickPi.Timeout = 150
		BrickPiSetTimeout()
		BrickPi.MotorSpeed[shootMotor] = 255		# turn the motor on to shoot
		BrickPiUpdateValues()
		
		root.bind_all('<Key>', keypress)			# read a key press to break the loop and go back to main menu
		root.withdraw()
		root.mainloop()		
		
while ans.lower() != "q":

	ans = raw_input("Input (Q to quit) : ")

	if  ans.lower() == "u":			# aim up
		up()
	elif ans.lower() == "d":		# aim down
		down()
	elif ans.lower() == "s":		# shoot
		shoot()
	
	
	#root.bind_all('<Key>', keypress)			# uncomment if we place the functions in the key press if-else branches
	#root.withdraw()
	#root.mainloop()		
	# maybe use threads to manage the motors running and key inputs?