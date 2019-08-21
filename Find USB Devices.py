import usb.core

#Devices values
DM70_VID=0x1447
DM70_PID=0x8092

RS232_VID=0x067B
RS232_PID=0x2303

#Code
dev = usb.core.find(idVendor=RS232_VID, idProduct=RS232_PID)
if dev is None:
    print ('ALERT our USB device is NOT connected')
else:
    print ('our USB device is connected')
