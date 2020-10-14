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

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

from .vlc_thread import VLCThread
from . import resources


class VLCWidget(QWidget):
    """Widget of the VLC application. It show a button map
    to all controls and it also displays information such as
    the current movie title, movie elapsed time and duration,
    and the volume of the vlc.

    Mappings:

    Pause/Play     - Num 5
    Volume up      - Num 8
    Volume down    - Num 2
    Back 5 sec     - Num 7
    Forward 5 sec  - Num 9
    Back 30 sec    - Num 1
    Forward 30 sec - Num 3
    Next track     - Num 6
    Previous track - Num 4
    """

    display_name = "Vlc"

    def __init__(self, main_window: "InfoPad") -> None:
        super().__init__()
        self.main_window = main_window
        self.data_thread = VLCThread(self.main_window.current_path)

        loadUi(f"{self.main_window.current_path}/widgets/vlc/vlc.ui", self)

        self.vlc_volume_meter.setMinimum(0)
        self.vlc_volume_meter.setMaximum(320)

    @staticmethod
    def get_icon(curr_path: str) -> QPixmap:
        return QPixmap(f"{curr_path}/widgets/vlc/vlc.png")

    def on_enter(self) -> None:
        """Connect signals and start thread"""
        self.data_thread.vlc_title.connect(self.update_title)
        self.data_thread.vlc_volume.connect(self.update_volume)
        self.data_thread.vlc_time.connect(self.update_time)
        self.data_thread.start()

    def update_title(self, title: str) -> None:
        """Update the title of playing movie"""
        self.title_label.setText(title)

    def update_volume(self, volume: int) -> None:
        """Update time slider and label"""
        self.vlc_volume_meter.setValue(volume)
        self.volume_label.setText(str(round(volume / 2.56)))

    def update_time(self, time: list) -> None:
        """Update elapsed time and duration of movie"""
        self.current_time.setText(time[0])
        self.movie_duration.setText(time[1])

    def on_exit(self) -> None:
        """Kill thread on exit"""
        self.data_thread.kill_thread()

    def grid_1(self) -> None:
        """Previous movie in playlist"""
        self.data_thread.prev()

    def grid_2(self) -> None:
        """Toggle play/pause"""
        self.data_thread.toggleplay()

    def grid_3(self) -> None:
        """Next movie in playlist"""
        self.data_thread.next()

    def grid_4(self) -> None:
        pass  # Num +

    def grid_5(self) -> None:
        """Jump backwards 30 sec"""
        self.data_thread.big_jump_backwars()

    def grid_6(self) -> None:
        """Turn down volume by 5%"""
        self.data_thread.volume_down()

    def grid_7(self) -> None:
        """Jump forwards 30 sec"""
        self.data_thread.big_jump_forwards()

    def grid_8(self) -> None:
        pass  # Num Enter

    def grid_9(self) -> None:
        """Jump forwards 5 sec"""
        self.data_thread.small_jump_forwards()

    def grid_sd(self) -> None:
        """Jump backwards 5 sec"""
        self.data_thread.small_jump_backwars()

    def grid_su(self) -> None:
        """Increase volume by 5 sec"""
        self.data_thread.volume_up()

    def grid_view_o(self) -> None:
        pass  # Num Page Down
