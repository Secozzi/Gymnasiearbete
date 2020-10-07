from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

from .vlc_thread import VLCThread


class VLCWidget(QWidget):
    """
    Control a vlc instance with global shortcuts. Mappings:

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

    def __init__(self, main_window) -> None:
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
        self.data_thread.vlc_title.connect(self.update_title)
        self.data_thread.vlc_volume.connect(self.update_volume)
        self.data_thread.vlc_time.connect(self.update_time)
        self.data_thread.start()

    def update_title(self, title: str) -> None:
        self.title_label.setText(title)

    def update_volume(self, volume: int) -> None:
        self.vlc_volume_meter.setValue(volume)
        self.volume_label.setText(str(round(volume / 2.56)))

    def update_time(self, time: list) -> None:
        self.current_time.setText(time[0])
        self.movie_duration.setText(time[1])

    def on_exit(self) -> None:
        self.data_thread.kill_thread()

    def grid_1(self) -> None:
        self.data_thread.prev()

    def grid_2(self) -> None:
        self.data_thread.toggleplay()

    def grid_3(self) -> None:
        self.data_thread.next()

    def grid_4(self) -> None:
        pass  # Num +

    def grid_5(self) -> None:
        self.data_thread.big_jump_backwars()

    def grid_6(self) -> None:
        self.data_thread.volume_down()

    def grid_7(self) -> None:
        self.data_thread.big_jump_forwards()

    def grid_8(self) -> None:
        pass  # Num Enter

    def grid_9(self) -> None:
        self.data_thread.small_jump_forwards()

    def grid_sd(self) -> None:
        self.data_thread.small_jump_backwars()

    def grid_su(self) -> None:
        self.data_thread.volume_up()

    def grid_view_o(self) -> None:
        pass  # Num Page Down
