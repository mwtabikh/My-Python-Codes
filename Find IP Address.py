import os
ip_address = "https://web.whatsapp.com/"

response = os.system("ping -c 1 " + ip_address)
#and then check the response...
if response == 0:
  print (ip_address, 'is up!')
else:
  print (ip_address, 'is not available!')
