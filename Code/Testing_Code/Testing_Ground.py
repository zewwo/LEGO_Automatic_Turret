''
# Basic Documentation goes here
''

# import every function from the BrickPi script
from BrickPi import *

# setup motor input
BrickPiSetup();

# obtain motor ports and initialize them
tiltMotor = PORT_A
BrickPi.MotorEnable[tiltMotor] = 1
shootMotor = PORT_B
BrickPi.MotorEnable[shootMotor] = 1

# obtain tilt(touch) sensors and initialize tilt sensors
tiltMin = PORT_1
BrickPi.SensorType[tiltMin] = TYPE_SENSOR_TOUCH
tiltMax = PORT_2
BrickPi.SensorType[tiltMax] = TYPE_SENSOR_TOUCH

# setup tilt sensors
BrickPiSetupSensors()

ans = "";


while ans.lower() != "q":
	# set the brick pi to stop at 5s
	BrickPi.Timeout = 5000
	BrickPiSetTimeout()

	print ""
	print "LEGO Turret Testing Grounds!"
	print ""
	print "Input T to test the Tilt Motor!"
	print "Input S to test the Shooting Motor!"
	print "Input min to test the tilt motor and it's tilt min!"
	print "Input max to test the tilt motor and it's tilt max!"
	print "Input Q to exit the Testing Ground!" 
	print ""

    ans = raw_input("Your input : ");
	if  ans.lower() == "t":
		tilt = ""
                        	        	        
		while tilt.lower() != "b":
			# set the brick pi to stop at 500ms
			BrickPi.Timeout = 500
			BrickPiSetTimeout()
			
			print ""
			print "Input U to go up (+y) or D to go down (-y)"
			print "or S to Stop the Motor or B to go back"
			print ""
			tilt = raw_input("Up or Down : ")
			
			if tilt.lower() == "u":
				BrickPi.MotorSpeed[tiltMotor] = -255    # go up
			elif tilt.lower() == "d":
				BrickPi.MotorSpeed[tiltMotor] = 255	    # go down
			elif tilt.lower() == "s":
				BrickPi.MotorSpeed[tiltMotor] = 0       # stop the motor
        		BrickPiUpdateValues()				# update tilt values
	
	
	BrickPiUpdateValues()
        
