#
#    My "Gymnasiearbete" for school 2020
#    Copyright (C) 2020 Folke Ishii
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from PyQt5.QtCore import pyqtSignal, QThread

from time import sleep
from GPUtil import getGPUs
from psutil import cpu_percent, virtual_memory


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
            _gpu = getGPUs()

            _gpu_load = round(_gpu[0].load*100, 1)
            _gpu_temp = _gpu[0].temperature
            _cpu_temp = 0
            _cpu_load = cpu_percent()
            _memory_load = virtual_memory().percent
            _ethernet_usage = 0

            self.system_info.emit([_gpu_load, _gpu_temp, _cpu_load, _cpu_temp, _memory_load, _ethernet_usage])
            sleep(self.system_refresh_rate)

    def kill_thread(self) -> None:
        self.thread_running = False
