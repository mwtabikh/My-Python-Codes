import os

def check_ip(ip_address):
    response = os.system("ping -c 1 " + ip_address)
    #and then check the response...
    if response == 0:
      print (ip_address, 'is up!')
      A=True
    else:
      print (ip_address, 'is not available')
      A=False
      B="IP address was not available"

ip_address="google.com"
check_ip(ip_address)