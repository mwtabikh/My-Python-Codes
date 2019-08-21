#Libraries
from main import *

#Objects Definiton
RM12 = Endurancet("google.com",0x1447,0x8092,"/dev/ttyUSB0",115200,serial.PARITY_NONE,1,8,1,
	M12,ALL,[0.2,2],M12,ETH,1,1)

RUSB = Endurancet("google.com",0x1447,0x8092,"/dev/ttyUSB0",115200,serial.PARITY_NONE,1,8,1,
	USB,ALL,[0.2,2],USB,ETH,1,1)

RETH = Endurancet("10.82.80.224",0x1447,0x8092,"/dev/ttyUSB0",115200,serial.PARITY_NONE,1,8,1,
	ETH,ALL,[0.2,2],ETH,M12,1,1)

try:
	logger.debug('test has started ')
	#checking device interfaces if are ok
	RM12.get_SERIALDATA()
	RUSB.check_USB()
	RETH.check_IP()
	#starting in pin testing
	RM12.test_INTERNAL()
	RM12.check_SERIAL()
	RUSB.test_INTERNAL()
	RUSB.check_USB()
	RETH.test_INTERNAL()
	RETH.check_IP()
	#Starting  inter cable testing
	#m12 vs eth cable test
	RM12.test_Cables()
	RM12.check_SERIAL()
	RETH.check_IP()
	#usb vs eth test
	RUSB.test_Cables()
	RETH.check_IP()
	RUSB.check_USB()
	#eth vs m12 test
	RETH.test_Cables()
	RM12.check_SERIAL()
	RETH.check_IP()
	#Random Testing
	RM12.lose_YOURMIND()
	RM12.check_SERIAL()
	RETH.check_IP()
	RUSB.check_USB()

except Exception as e: #general exceptions
	logger.error('Something went wrong' + str(e))

else:#goes here if no exception were thrown
	logger.debug('everything was successfully executed')

finally:#always goes here after finishing from script
	logger.debug('test has ended')

#Exit cleanout
GPIO.cleanup()