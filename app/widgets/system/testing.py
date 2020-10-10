import psutil
import GPUtil
from time import sleep

import requests
_ok = requests.get("http://127.0.0.1:5200")
print(_ok)

#while True:
#    _gpu = GPUtil.getGPUs()
#    print(_gpu[0].load*100)
#    print(_gpu[0].temperature)
#    sleep(1)