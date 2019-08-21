import time
import serial

#Setting COM Ports
port_name= '/dev/ttyUSB0',
baud_rate=115200,
serial_parity=serial.PARITY_NONE,
stop_bits=serial.STOPBITS_ONE,
byte_size=serial.EIGHTBITS,
time_out=1

#Code
print ("Starting program")

ser = serial.Serial(
    port= port_name,
    baudrate=baud_rate,
    parity=serial_parity,
    stopbits=stop_bits,
    bytesize=byte_size,
    timeout=time_out
    )
time.sleep(1)
try:
    ser.write("help\r\n".encode())
    while True:
        if ser.inWaiting() > 0:
            data = ser.readline()
            print (data)
        
except KeyboardInterrupt:
    print ("Exiting Program")

except:
    print ("Error Occurs, Exiting Program")

finally:
    ser.close()
    pass