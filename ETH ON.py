#Libraries and warnings
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#setting GPIO pins
M12 = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5 , 6, 13]
USB = [19,26,20,21,18,23,24,25,8,7]
ETH = [12,14,15,16]

while True:
    for i in ETH:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)
        GPIO.output(i, GPIO.LOW)
#GPIO pin Reset
GPIO.cleanup()
