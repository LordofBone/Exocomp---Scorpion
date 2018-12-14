#thanks to https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/using-the-python-library
#for some code

#!/user/bin/env python3
from picamera import PiCamera
import subprocess
import time
import sys
import subprocess
import serial
import Adafruit_PCA9685

#setting up serial
port = "/dev/ttyACM0"

s1 = serial.Serial(port,9600)

s1.flushInput()

#setting up camera/servos
camera = PiCamera()

pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
#right servo
servo_max1 = 470  # Max pulse length out of 4096
servo_min1 = 300  # Min pulse length out of 4096

#left servo
servo_max2 = 250  # Max pulse length out of 4096
servo_min2 = 420  # Min pulse length out of 4096


# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)


while True:
	if("object_detected" in str(s1.readline())):
		print ("object detected")
		camera.start_preview()
		time.sleep(1)
		#capture photo from camera to file
		camera.capture('/home/pi/image.jpg')
		camera.stop_preview()
		
		#pass the photo into tensorflow image recognition
		commandOutput = subprocess.getoutput(["python3 /home/pi/vision/models/tutorials/image/imagenet/classify_image.py --image_file=/home/pi/image.jpg --model_dir=/home/pi/imagenet --num_top_predictions=1"])
		
		#get the top predictions and score and strip out any newlines
		topPrediction = str(commandOutput.split("kwds)")[2])
		topPrediction = topPrediction.strip('\n')
		
		print(topPrediction)
		
		time.sleep(5)
		
		#send top prediction via telegram
		subprocess.call(['./telegram_send.sh', topPrediction])
		
		continue
	
	#this will close the pincers
	if("servo_move_grab" in str(s1.readline())):
		print ("grabbing")
		#right servo
		pwm.set_pwm(0, 0, servo_max1)
		time.sleep(1)
		#left servo
		pwm.set_pwm(1, 0, servo_max2)
		time.sleep(1)
	
	#this will open the pincers
	if("servo_move_letgo" in str(s1.readline())):
		print ("letting go")
		#right servo
		pwm.set_pwm(0, 0, servo_min1)
		time.sleep(1)
		#left servo
		pwm.set_pwm(1, 0, servo_min2)
		time.sleep(1)
	
	#switch off the pi
	if("switchoff" in str(s1.readline())):
		print ("switching off")
		subprocess.call('sudo shutdown now', shell=True)
	else:
		continue		
