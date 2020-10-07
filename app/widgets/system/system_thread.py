from PyQt5.QtCore import pyqtSignal, QThread
from time import sleep
import psutil
import GPUtil


class SystemThread(QThread):
    """Thread to get system information

    Signals:
    system_info: list
        [gpu_load, gpu_temp, cpu_load, cpu_temp, mem_usage, ethernet_usage]
    """

    system_info = pyqtSignal(list)
    system_refresh_rate = 1

    def run(self) -> None:

        self.thread_running = True

        while self.thread_running:
            # Do stuff
            sleep(self.system_refresh_rate)

    def kill_thread(self) -> None:
            self.thread_running = False
