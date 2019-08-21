#Libraries and warnings
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#setting GPIO pins
M12 = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5 , 6, 13]
USB = [19,26,20,21,18,23,24,25,8,7]
ETH = [12,14,15,16]
ALL = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5 , 6, 13, 9, 26, 20, 21, 18, 23, 24, 25, 8, 7, 12, 14, 15, 16]

def test_cables(cable_1, cable_2,sleep):
   while True:
        for l in sleep:
           for i in cable_1:
            GPIO.setup(i,GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)
            GPIO.output(i,GPIO.LOW)
            for j in cable_2:
                GPIO.setup(j,GPIO.OUT)
                GPIO.output(j, GPIO.HIGH)
                GPIO.output(j,GPIO.LOW)  
                time.sleep(l)
                GPIO.output(j,GPIO.HIGH)
            GPIO.output(i,GPIO.HIGH)

sleep=[0.2,1]
cable_1=M12
cable_2=USB
test_cables(cable_1, cable_2, sleep)

GPIO.cleanup()
