import usb.core

def check_usb(vid,pid):
    dev = usb.core.find(idVendor=vid, idProduct= pid)
    if dev is None:
        A=False
        B="USB Device was not connected"
        print ('ALERT our USB device is NOT connected')
    else:
        A=True
        print ('our USB device is connected')

vid=0x1447
pid=0x8092

check_usb(vid,pid)