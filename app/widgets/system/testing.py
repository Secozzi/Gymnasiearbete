import psutil
import GPUtil
from time import sleep

while True:
    print(psutil.cpu_percent(interval=0.0))
    sleep(1)