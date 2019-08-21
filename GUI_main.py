#libraries and warnings
import os
import usb.core
import time
import random
import serial
from tkinter import *
import logging
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
A=1
def turn_ON(cable): #turns ON a cable, VAR: Cable name 
    t1='turning ON Cable'
    logger.debug(t1)
    for i in cable:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)
        GPIO.output(i, GPIO.LOW)
    time.sleep(40)

def turn_OFF(offcable=ALL):#turns off a cable, VAR: Cable name 
    for i in offcable:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)
        
def check_IP(ip_address='10.82.80.224'):#pings ip address, VAR(Variables): IP address 
    logger.debug('checking ip address')
    turn_ON(ETH)
    response = os.system("ping -c 1 " + ip_address)
    #and then check the response...
    if response == 0:
        logger.debug(ip_address + ' was available')
    else:
        logger.debug (ip_address + ' was not available')
        raise device_crashed(" Device Crashed")
    turn_OFF()
    time.sleep(1)

def check_USB(vid=0x1447,pid=0x8092):#pings usb device, VAR: VID & PID of device
    logger.debug('checking USB Connection')
    turn_ON(USB)
    dev = usb.core.find(idVendor= vid, idProduct= pid)
    if dev is None:
        logger.debug ('ALERT our USB device is NOT connected')
        print(vid + ' '+pid)
        raise device_crashed(" Device Crashed")
    else:
        logger.debug('our USB device is connected') 
    turn_OFF()
    time.sleep(1)

def check_SERIAL(port_name='/dev/TTYUSB0',baud_rate=115200,serial_parity='serial.PARITY_NONE',stop_bits=8,byte_size=8,time_out=1): #pings serial interface, VAR: port name, baud rate, parity, stopB, byteS, Timeout
    logger.debug('checking Serial Connection')
    turn_ON(M12)
    ser = serial.Serial(
        port=port_name,
        baudrate=baud_rate,
        parity=serial_parity,
        stopbits=stop_bits,
        bytesize=byte_size,
        timeout=time_out
        )
    time.sleep(1)
    A=0
    try:
        ser.write("||;1>get logfile\r\n".encode())
        for x in range(0,1000):
            if ser.inWaiting() > 10:
                A=1
    finally:
        ser.close()
        if A==0:
            raise device_crashed(" Device Crashed")
        turn_OFF()
        time.sleep(1)

def test_CABLES(sleep,cable_1,cable_2): #tests 2 cables or 1 together, VAR: sleep (2x1 array), cable 1, cable 2 
    logger.debug('inter cable test starting')
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
    time.sleep(30)
    logger.debug('inter cable test finished')

def test_INTERNAL(sleep,cable): #tests 1 cable together, VAR: sleep (2x1 array), cable 1, cable 2 
    logger.debug('single cable test starting')
    for l in sleep:
            for i in cable:
                GPIO.setup(i,GPIO.OUT)
                GPIO.output(i, GPIO.HIGH)
                GPIO.output(i,GPIO.LOW)
                for j in cable:
                    GPIO.setup(j,GPIO.OUT)
                    GPIO.output(j, GPIO.HIGH)
                    GPIO.output(j,GPIO.LOW)  
                    time.sleep(l)
                    GPIO.output(j,GPIO.HIGH)
                GPIO.output(i,GPIO.HIGH)
    time.sleep(30)
    logger.debug('Intercable test finished')

def lose_YOURMIND(testing_time): #random cable testing, VAR= time in minutes 
    logger.debug('Random test starting')
    t_end= time.time() + testing_time*60
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
#GUI Code
HEIGHT=600
WIDTH=750

root = Tk()
root.title('DM280 Endurance Test')

canvas = Canvas(root, height=HEIGHT, width=WIDTH,bg='white') #i can use #hex nb for color code
canvas.grid()
backg_image =PhotoImage(file='/home/pi/Desktop/DM280_ET/top.png')
canvas.create_image(0,0,anchor=NW, image=backg_image)

frame = Frame(root,bg='#808080',bd=5)
frame.place(relx=0.5,rely=0.14,relwidth=0.8,relheight=0.4, anchor='n')

label = Label(frame, bg='white')
label.place(relx=0.005,rely=0.01, relwidth=0.99, relheight=0.72)
label = Label(frame,text='Test Settings:', bg='white',font='arial 12 underline')
label.grid(row=1,padx=10,pady=5)
label2 = Label(frame,text='Relay switching Time:', bg='white')
label2.grid(row=2,column=2,padx=10,pady=5)
label3 = Label(frame,text='Random Test Time:', bg='white')
label3.grid(row=2,column=3,padx=10,pady=5)
label4 = Label(frame,text='Slow:', bg='white')
label4.place(relx=0.245,rely=0.28,relwidth=0.1,relheight=0.1)
label4 = Label(frame,text='Fast:', bg='white')
label4.place(relx=0.245,rely=0.4,relwidth=0.1,relheight=0.1)
label4 = Label(frame,text='Sec', bg='white')
label4.place(relx=0.36,rely=0.28,relwidth=0.1,relheight=0.1)
label4 = Label(frame,text='Sec', bg='white')
label4.place(relx=0.36,rely=0.4,relwidth=0.1,relheight=0.1)
label4 = Label(frame,text='Min', bg='white')
label4.place(relx=0.6,rely=0.33,relwidth=0.1,relheight=0.1)

time_OUT = Text(frame, bg='#ffff80')
time_OUT.place(relx=0.76,rely=0.32,relwidth=0.19,relheight=0.31)

entry_FASTT = Entry(frame, bg="white")
entry_FASTT.place(relx=0.33,rely=0.28,relwidth=0.05,relheight=0.1)
entry_SLOWT = Entry(frame, bg="white")
entry_SLOWT.place(relx=0.33,rely=0.4,relwidth=0.05,relheight=0.1)
entry_RANDT = Entry(frame, bg="white")
entry_RANDT.place(relx=0.52,rely=0.33,relwidth=0.1,relheight=0.1)

def calculate_TIME():
    float_a=entry_FASTT.get()
    float_b=entry_SLOWT.get()
    t=float_a+float_b
    test1=29*float(t) + 90 #29 is the nb of pins, 90 is the times the test has been repeated
    test2= 221*float(t)+90 #221 is the pins repetition nb
    approx= float(entry_RANDT.get())*60 + float(test1) + float(test2)
    day= approx // (24*3600)
    approx=approx % (24*3600)
    hour=approx //3600
    approx %= 3600
    minutes = approx//60
    text=str(round(day,2)) +' day(s)\n' + str(hour) +' hour(s)\n' + str(minutes) +' minute(s)'
    time_OUT.delete(0.0,'end')
    time_OUT.insert(0.0,text)
    logger.debug('Time required for test to take place is: ')
    logger.debug(text)
        
label5 = Button(frame,text='Calculate Test Time', bg='white',command=calculate_TIME)
label5.grid(row=2,column=4,padx=0)

T1=IntVar()
T2=IntVar()
T3=IntVar()
checkbt1=Checkbutton(frame,text='Inter Pin Test    ',bg='white',variable=T1)
checkbt1.grid(row=2,padx=5,pady=5)
checkbt2=Checkbutton(frame,text='Inter Cable Test', bg='white',variable=T2)
checkbt2.grid(row=3,padx=0,pady=5)
checkbt3=Checkbutton(frame,text='Random Test    ', bg='white',variable=T3)
checkbt3.grid(row=4,padx=0,pady=5)

second_frame = Frame(root,bg='#808080',bd=5)
second_frame.place(relx=0.5,rely=0.44,relwidth=0.8,relheight=0.4, anchor='n')

label = Label(second_frame, bg='white')
label.place(relx=0.005,rely=0.01, relwidth=0.99, relheight=0.92)
label = Label(second_frame, text='Device Info:',borderwidth=1, bg='white',font='arial 12 underline')
label.grid(row=1,column=0,padx=0,pady=15)
label = Label(second_frame, text='IP Address:',borderwidth=1, bg='white')
label.grid(row=4,column=0,padx=0,pady=5)
label = Label(second_frame, text='USB Settings:',borderwidth=1, bg='white')
label.grid(row=6,column=0,padx=15,pady=5)
label = Label(second_frame, text='VID',borderwidth=1, bg='white')
label.grid(row=8,column=0,padx=0,pady=5)
label = Label(second_frame, text='PID',borderwidth=1, bg='white')
label.grid(row=10,column=0,padx=0,pady=5)

entry_IP = Entry(second_frame, bg="white")
entry_IP.grid(row=4,column=1,padx=0,pady=5)
entry_VID = Entry(second_frame, bg="white")
entry_VID.grid(row=8,column=1,padx=0,pady=5)
entry_PID = Entry(second_frame, bg="white")
entry_PID.grid(row=10,column=1,padx=0,pady=5)

label = Label(second_frame, text='ex:10.82.80.225',borderwidth=1, bg='white')
label.grid(row=4,column=3,padx=15,pady=5)
label = Label(second_frame, text='ex: 0x1447',borderwidth=1, bg='white')
label.grid(row=8,column=3,padx=0,pady=5)
label = Label(second_frame, text='ex: 0x8203',borderwidth=1, bg='white')
label.grid(row=10,column=3,padx=0,pady=5)

#Code
Slow_Fast=[entry_SLOWT,entry_FASTT]

def start_testing():
    try:
        logger.debug('test has started ')
        #checking device interfaces if are ok
        check_SERIAL()
        check_USB(int(entry_VID.get(),16),int(entry_PID.get(),16))
        check_IP(ip_address=entry_IP.get())
       
        #starting in pin testing
        if T1==True:
            test_INTERNAL(M12)
            check_SERIAL()
            test_INTERNAL(USB)
            check_USB(int(entry_VID.get(),16),int(entry_PID.get(),16))
            test_INTERNAL(ETH)
            check_IP(ip_address=entry_IP.get())
        #Starting  inter cable testing
        #m12 vs eth cable test
        if T2==True:
            test_Cables(M12,ETH)
            check_SERIAL()
            check_IP(ip_address=entry_IP.get())
            #usb vs eth test
            test_Cables(USB,ETH)
            check_IP(ip_address=entry_IP.get())
            check_USB(int(entry_VID.get(),16),int(entry_PID.get(),16))
            #eth vs m12 test
            test_Cables(USB,M12)
            check_SERIAL()
            check_USB(int(entry_VID.get(),16),int(entry_PID.get(),16))
        #Random Testing
        if T3==True:
            lose_YOURMIND(entry_RANDT.get())
            check_SERIAL()
            check_IP(ip_address=entry_IP.get())
            check_USB(int(entry_VID.get(),16),int(entry_PID.get(),16))

    except Exception as e: #general exceptions
        logger.error('Something went wrong: ' + str(e))
        turn_OFF()
    else:#goes here if no exception were thrown
        logger.debug('everything was successfully executed')

    finally:#always goes here after finishing from script
        logger.debug('test has ended')
        
button=Button(second_frame, text='Start Test',borderwidth=10,command= start_testing)
button.place(relx=0.8,rely=0.32,relwidth=0.15,relheight=0.22)

root.mainloop()

#Exit cleanout
GPIO.cleanup()