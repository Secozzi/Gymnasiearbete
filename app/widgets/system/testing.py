import psutil
import GPUtil
from time import sleep

while True:
    print(psutil.cpu_percent())
    sleep(0.5)


print(psutil.virtual_memory().percent)
GPUtil.showUtilization()