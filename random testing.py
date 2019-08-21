#Libraries and warnings
import RPi.GPIO as GPIO
import time
import random
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#setting GPIO pins
M12 = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5 , 6, 13]
USB = [19,26,20,21,18,23,24,25,8,7]
ETH = [12,14,15,16]
ALL = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5 , 6, 13, 9, 26, 20, 21, 18, 23, 24, 25, 8, 7, 12, 14, 15, 16]

for i in ALL:
        GPIO.setup(i,GPIO.OUT)

def lose_your_mind(test_time): #input test time in minutes
    t_end= time.time() + test_time*60
    while time.time() < t_end:
        c=random.randint(1,25) #random pin
        d=random.randint(1,25)
        l=random.randint(0,4) #random time
        t=random.randint(0,4)
        
        GPIO.setup(c,GPIO.OUT)
        GPIO.setup(d,GPIO.OUT)

        GPIO.output(c, GPIO.HIGH)
        GPIO.output(c,GPIO.LOW) 
        time.sleep(l)

        GPIO.output(d, GPIO.HIGH)
        GPIO.output(d,GPIO.LOW) 
        time.sleep(t)
        
        GPIO.output(c, GPIO.HIGH)
        GPIO.output(d, GPIO.HIGH)

test_time = 1
lose_your_mind(test_time)

GPIO.cleanup()

