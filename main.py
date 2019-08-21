#libraries and warnings
import os
import usb.core
import time
import random
import serial
import logging #debug, warning, error and critical not info
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#logger Config, for log msg format: logRec attributes pyth
logger= logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('DM280 Endurance test log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')
stream_handler=logging.StreamHandler()
logger.addHandler(stream_handler)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#GPIO PINS Pinout for cables
M12 = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5 , 6, 13]
USB = [19,26,20,21,18,23,24,25,8,7]
ETH = [12,14,15,16]
ALL = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5 , 6, 13, 9, 26, 20, 21, 18, 23, 24, 25, 8, 7, 12, 14, 15, 16]

#Class and funtions definiton
class device_crashed(Exception):
	pass
 
class Endurancet:
	def __init__(self,ip_address,vid,pid,port_name,baud_rate,serial_parity,stop_bits,byte_size,time_out,
		cable,offcable,sleep,cable_1,cable_2,testing_time,A=1):
		self.ip_address=ip_address
		self.vid=vid
		self.pid=pid
		self.port_name=port_name
		self.baud_rate=baud_rate
		self.serial_parity=serial_parity
		self.stop_bits=stop_bits
		self.byte_size=byte_size
		self.time_out=time_out
		self.cable=cable
		self.offcable=offcable
		self.sleep=sleep
		self.cable_1=cable_1
		self.cable_2=cable_2
		self.testing_time=testing_time
		self.__A = A

	#Setter and getter for A
	def get_A(self):
		return self.__A

	def set_A(self, A):
		self.__A = A

	#Functions definition
	def check_IP(self):#pings ip address, VAR(Variables): IP address 
		logger.debug('checking ip address')
		self.turn_ON()
		response = os.system("ping -c 1 " + self.ip_address)
		#and then check the response...
		if response == 0:
			logger.debug(self.ip_address + ' was available')
		else:
			logger.debug (self.ip_address + ' was not available')
			raise device_crashed(" Device Crashed")
		self.turn_OFF()
		time.sleep(1)

	def check_USB(self):#pings usb device, VAR: VID & PID of device
		logger.debug('checking USB Connetion')
		self.turn_ON()
		dev = usb.core.find(idVendor=self.vid, idProduct= self.pid)
		if dev is None:
			logger.debug ('ALERT our USB device is NOT connected')
			raise device_crashed(" Device Crashed")
		else:
			logger.debug('our USB device is connected') 
		self.turn_OFF()
		time.sleep(1)

	def get_SERIALDATA(self): #pings serial interface, VAR: port name, baud rate, parity, stopB, byteS, Timeout
		logger.debug('checking Serial Connection')
		self.turn_ON()
		ser = serial.Serial(
			port=self.port_name,
			baudrate=self.baud_rate,
			parity=self.serial_parity,
			stopbits=self.stop_bits,
			bytesize=self.byte_size,
			timeout=self.time_out
			)
		time.sleep(1)
		self.set_A(0)
		try:
			ser.write("||;1>get logfile\r\n".encode())
			logger.debug("This is the data i got :")
			for x in range(0,1000):
				if ser.inWaiting() > 10:
					data = ser.readline()
					logger.debug(data)
					self.set_A(1)
		finally:
			ser.close()
			if self.get_A()==0:
				raise device_crashed(" Device Crashed")
			self.turn_OFF()
			time.sleep(1)

	def check_SERIAL(self): #pings serial interface, VAR: port name, baud rate, parity, stopB, byteS, Timeout
		logger.debug('checking Serial Connection')
		self.turn_ON()
		ser = serial.Serial(
			port=self.port_name,
			baudrate=self.baud_rate,
			parity=self.serial_parity,
			stopbits=self.stop_bits,
			bytesize=self.byte_size,
			timeout=self.time_out
			)
		time.sleep(1)
		self.set_A(0)
		try:
			ser.write("||;1>get logfile\r\n".encode())
			logger.debug("This is the data i got :")
			for x in range(0,1000):
				if ser.inWaiting() > 10:
					self.set_A(1)
		finally:
			ser.close()
			if self.get_A()==0:
				raise device_crashed(" Device Crashed")
			self.turn_OFF()
			time.sleep(1)

	def turn_ON(self): #turns ON a cable, VAR: Cable name 
		logger.debug('turning ON Cable')
		for i in self.cable:
			GPIO.setup(i, GPIO.OUT)
			GPIO.output(i, GPIO.HIGH)
			GPIO.output(i, GPIO.LOW)
		time.sleep(30)

	def turn_OFF(self):#turns off a cable, VAR: Cable name 
		for i in self.offcable:
			GPIO.setup(i, GPIO.OUT)
			GPIO.output(i, GPIO.HIGH)

	def test_CABLES(self): #tests 2 cables or 1 together, VAR: sleep (2x1 array), cable 1, cable 2 
		logger.debug('inter cable test starting')
		for l in self.sleep:
			for i in self.cable_1:
				GPIO.setup(i,GPIO.OUT)
				GPIO.output(i, GPIO.HIGH)
				GPIO.output(i,GPIO.LOW)
				for j in self.cable_2:
					GPIO.setup(j,GPIO.OUT)
					GPIO.output(j, GPIO.HIGH)
					GPIO.output(j,GPIO.LOW)  
					time.sleep(l)
					GPIO.output(j,GPIO.HIGH)
				GPIO.output(i,GPIO.HIGH)
		time.sleep(30)
		logger.debug('inter cable test finished')

	def test_INTERNAL(self): #tests 1 cable together, VAR: sleep (2x1 array), cable 1, cable 2 
		logger.debug('single cable test starting')
		for l in self.sleep:
				for i in self.cable:
					GPIO.setup(i,GPIO.OUT)
					GPIO.output(i, GPIO.HIGH)
					GPIO.output(i,GPIO.LOW)
					for j in self.cable:
						GPIO.setup(j,GPIO.OUT)
						GPIO.output(j, GPIO.HIGH)
						GPIO.output(j,GPIO.LOW)  
						time.sleep(l)
						GPIO.output(j,GPIO.HIGH)
					GPIO.output(i,GPIO.HIGH)
		time.sleep(30)
		logger.debug('Intercable test finished')

	def lose_YOURMIND(self): #random cable testing, VAR= time in minutes 
		logger.debug('Random test starting')
		t_end= time.time() + self.testing_time*60
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
		logger.debug('Random test finished')