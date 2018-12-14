#!/user/bin/env python3
from picamera import PiCamera
import subprocess
import time
import sys
import subprocess
import serial
import Adafruit_PCA9685

port = "/dev/ttyACM0"

s1 = serial.Serial(port,9600)

s1.flushInput()

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
		camera.capture('/home/pi/image.jpg')
		camera.stop_preview()
		
		commandOutput = subprocess.getoutput(["python3 /home/pi/vision/models/tutorials/image/imagenet/classify_image.py --image_file=/home/pi/image.jpg --model_dir=/home/pi/imagenet --num_top_predictions=1"])
		
		topPrediction = str(commandOutput.split("kwds)")[2])
		topPrediction = topPrediction.strip('\n')
		
		print(topPrediction)
		
		time.sleep(5)
		
		subprocess.call(['./telegram_send.sh', topPrediction])
		
		continue

	if("servo_move_grab" in str(s1.readline())):
		print ("grabbing")
		#right servo
		pwm.set_pwm(0, 0, servo_max1)
		time.sleep(1)
		#left servo
		pwm.set_pwm(1, 0, servo_max2)
		time.sleep(1)
		
	if("servo_move_letgo" in str(s1.readline())):
		print ("letting go")
		#right servo
		pwm.set_pwm(0, 0, servo_min1)
		time.sleep(1)
		#left servo
		pwm.set_pwm(1, 0, servo_min2)
		time.sleep(1)
				
	if("switchoff" in str(s1.readline())):
		print ("switching off")
		subprocess.call('sudo shutdown now', shell=True)
	else:
		continue		
