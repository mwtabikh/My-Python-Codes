#Libraries and warnings
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#setting GPIO pins
M12 = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5 , 6, 13]
USB = [19,26,20,21,18,23,24,25,8,7]
ETH = [12,14,15,16]
ALL = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5 , 6, 13, 9, 26, 20, 21, 18, 23, 24, 25, 8, 7, 12, 14, 15, 16]

def Turn_OFF(offcable):
    while True:
        for i in cable:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)
    GPIO.cleanup()

offcable = ALL
Turn_OFF(offcable)