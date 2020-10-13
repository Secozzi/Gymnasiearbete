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

from socket import socket, AF_INET, SOCK_STREAM, gethostbyname
from time import sleep
from json import loads, decoder
from GPUtil import getGPUs


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
        self.socket = socket(AF_INET, SOCK_STREAM)

        ip = gethostbyname("127.0.0.1")
        port = 5200

        self.address = (ip, port)
        self.socket.connect(self.address)

        while self.thread_running:
            try:
                _data = self.socket.recv(1024)
                data = loads(_data.strip())
            except decoder.JSONDecodeError:
                print("It failed lmao")
                data = data
            _gpu = getGPUs()

            _gpu_load = round(_gpu[0].load*100, 1)
            _gpu_temp = _gpu[0].temperature
            _cpu_temp = round(max(data["CpuInfo"]["fTemp"]))
            _cpu_load = round(sum(data["CpuInfo"]["uiLoad"]) / data["CpuInfo"]["uiCoreCnt"])
            _memory_load = data["MemoryInfo"]["MemoryLoad"]
            _ethernet_usage = 0

            self.system_info.emit([_gpu_load, _gpu_temp, _cpu_load, _cpu_temp, _memory_load, _ethernet_usage])
            print("Running")
            sleep(self.system_refresh_rate)

    def kill_thread(self) -> None:
        self.thread_running = False
