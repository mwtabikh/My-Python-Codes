import time
import serial

def check_serial(port_name, baud_rate,serial_parity,stop_bits,byte_size,time_out):
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
                print("Serial is up !")
                print (data)
                A=True
            else:
                A=False
                print("Serial is down")

    finally:
        ser.close()
        pass
    
port_name= "/dev/ttyUSB0"
baud_rate=115200
serial_parity=serial.PARITY_NONE
stop_bits=serial.STOPBITS_ONE
byte_size=serial.EIGHTBITS
time_out=1

check_serial(port_name, baud_rate,serial_parity,stop_bits,byte_size,time_out)
