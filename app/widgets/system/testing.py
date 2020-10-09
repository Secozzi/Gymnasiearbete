import psutil
from time import sleep
import wmi


while True:
    w = wmi.WMI()
    print(w.Win32_TemperatureProbe()[0].CurrentReading)
    sleep(1)