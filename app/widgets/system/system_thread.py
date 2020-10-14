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

from time import sleep, time
from GPUtil import getGPUs
from psutil import cpu_percent, virtual_memory, net_io_counters


class SystemThread(QThread):
    """Thread to get system information

    Signals:
    system_info: list
        [gpu_load, gpu_temp, cpu_load, mem_usage,
        [eth_in_str, eth_in_int], [eth_out_str, eth_out_int]]
    """

    system_info = pyqtSignal(list)
    system_refresh_rate = 1

    @staticmethod
    def humanbits(B: int) -> list:
        """Converts bits into human readable form and percent of 100Mbits

        :param B: int
            Bits
        :return: list
            List containing redable form and perecnt of 100Mbits in that order
        """
        B = float(B)
        KB = float(1024)
        MB = float(KB ** 2)  # 1,048,576
        GB = float(KB ** 3)  # 1,073,741,824
        TB = float(KB ** 4)  # 1,099,511,627,776
        _bits = int(B / KB)

        if B < KB:
            return ["{0} {1}".format(B, "Bits" if 0 == B > 1 else "Bit"), _bits]
        elif KB <= B < MB:
            return ["{0:.2f} Kbit/s".format(B / KB), _bits]
        elif MB <= B < GB:
            return ["{0:.2f} Mbit/s".format(B / MB), _bits]
        elif GB <= B < TB:
            return ["{0:.2f} Gbit/s".format(B / GB), _bits]
        elif TB <= B:
            return ["{0:.2f} Tbit/s".format(B / TB), _bits]

    def run(self) -> None:

        self.thread_running = True
        network_card = "Ethernet 2"

        _ul = 0.0
        _dl = 0.0
        _t0 = time()

        _upload = net_io_counters(pernic=True)[network_card][0]
        _download = net_io_counters(pernic=True)[network_card][1]
        _up_down = (_upload, _download)

        while self.thread_running:
            _gpu = getGPUs()

            _gpu_load = round(_gpu[0].load * 100, 1)
            _gpu_temp = _gpu[0].temperature
            _cpu_load = cpu_percent()
            _memory_load = virtual_memory().percent

            _last_up_down = _up_down
            _upload = net_io_counters(pernic=True)[network_card][0]
            _download = net_io_counters(pernic=True)[network_card][1]
            _up_down = (_upload, _download)

            _t1 = time()
            _ul, _dl = [
                (_now - _last) / (_t1 - _t0)
                for _now, _last in zip(_up_down, _last_up_down)
            ]
            _t0 = time()

            _ul_l = self.humanbits(_ul * 8)
            _dl_l = self.humanbits(_dl * 8)

            self.system_info.emit(
                [_gpu_load, _gpu_temp, _cpu_load, _memory_load, _dl_l, _ul_l]
            )
            sleep(self.system_refresh_rate)

    def kill_thread(self) -> None:
        self.thread_running = False
