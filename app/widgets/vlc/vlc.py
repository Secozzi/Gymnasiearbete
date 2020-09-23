from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

from telnetlib import Telnet
from socket import error as socketerror
from configparser import ConfigParser
from time import sleep


class VLCController:
    def __init__(self, host: str, port: int) -> None:
        self.vlc_running = False

        try:
            self.tn = Telnet(host, port)
        except socketerror:
            self.vlc_running = False
        else:
            self.vlc_running = True

    def set_password(self, password: str) -> None:
        self.tn.read_until(b"Password: ")
        self.run_command(password)

    def run_command(self, command: str) -> list:
        self.tn.write(command.encode("utf-8") + b"\n")

        output = self.tn.read_until(b"> ").decode("utf-8")
        return output.split("\r\n")[:-1]

    def get_length(self) -> int:
        return int(self.run_command("get_length")[0])

    def get_time(self) -> int:
        return int(self.run_command("get_time")[0])

    def toggleplay(self) -> None:
        self.run_command("pause")

    def volume(self) -> int:
        return int(self.run_command("volume")[0])

    def volume_up(self) -> None:
        self.run_command("volup 1")

    def volume_down(self) -> None:
        self.run_command("voldown 1")

    def small_jump_forwards(self) -> None:
        if self.get_time() + 5 < self.get_length():
            self.run_command(f"seek {self.get_time() + 5}")

    def small_jump_backwars(self) -> None:
        if self.get_time() - 5 > 0:
            self.run_command(f"seek {self.get_time() - 5}")

    def big_jump_forwards(self) -> None:
        if self.get_time() + 30 < self.get_length():
            self.run_command(f"seek {self.get_time() + 30}")

    def big_jump_backwars(self) -> None:
        if self.get_time() - 30 > 0:
            self.run_command(f"seek {self.get_time() - 30}")

    def next(self) -> None:
        self.run_command("next")

    def prev(self) -> None:
        self.run_command("prev")


class VLCWidget(QWidget):
    """
    Control a vlc instance with global shortcuts. Shortcuts:

    Pause/Play      - Ctrl + Alt + Shift + 1 - Num 5
    Volume up       - Ctrl + Alt + Shift + 2 - Num 8
    Volume down     - Ctrl + Alt + Shift + 3 - Num 2
    Back 5 sec      - Ctrl + Alt + Shift + 4 - Num 7
    Forward 5 sec   - Ctrl + Alt + Shift + 5 - Num 9
    Back 30 sec     - Ctrl + Alt + Shift + 6 - Num 1
    Forward 30 sec  - Ctrl + Alt + Shift + 7 - Num 3
    Next track      - Ctrl + Alt + Shift + 8 - Num 6
    Previous track  - Ctrl + Alt + Shift + 9 - Num 4
    """

    display_name = "Vlc"

    def __init__(self, main_window) -> None:
        super().__init__()
        self.main_window = main_window

        loadUi(f"{self.main_window.current_path}/widgets/vlc/vlc.ui", self)

        self.vlc_volume_meter.setMinimum(0)
        self.vlc_volume_meter.setMaximum(320)

    @staticmethod
    def get_icon(curr_path: str) -> QPixmap:
        return QPixmap(f"{curr_path}/widgets/vlc/vlc.png")

    def on_enter(self) -> None:
        self.vlc_app = VLCController("127.0.0.1", 4212)
        self.vlc_running = self.vlc_app.vlc_running
        if self.vlc_running:
            credentials = ConfigParser()
            credentials.read(f"{self.main_window.current_path}/credentials.cfg")
            vlc_password = credentials["VLC"]["PASSWORD"]

            self.vlc_app.set_password(vlc_password)

            self.title_label.setText(self.vlc_app.run_command("get_title")[0])
            self.vlc_volume_meter.setValue(self.vlc_app.volume())
            self.volume_label.setText(str(round(self.vlc_app.volume() / 2.56)))
        else:
            self.title_label.setText("VLC not running")

    def on_exit(self) -> None:
        pass  # Call on exit

    def grid_1(self) -> None:
        self.vlc_app.prev()
        sleep(0.1)
        self.title_label.setText(self.vlc_app.run_command("get_title")[0])

    def grid_2(self) -> None:
        self.vlc_app.toggleplay()

    def grid_3(self) -> None:
        self.vlc_app.next()
        sleep(0.1)
        self.title_label.setText(self.vlc_app.run_command("get_title")[0])

    def grid_4(self) -> None:
        pass  # Num +

    def grid_5(self) -> None:
        self.vlc_app.big_jump_backwars()

    def grid_6(self) -> None:
        self.vlc_app.volume_down()
        self.vlc_volume_meter.setValue(self.vlc_app.volume())
        self.volume_label.setText(str(round(self.vlc_app.volume() / 2.56)))

    def grid_7(self) -> None:
        self.vlc_app.big_jump_forwards()

    def grid_8(self) -> None:
        pass  # Num Enter

    def grid_9(self) -> None:
        self.vlc_app.small_jump_forwards()

    def grid_sd(self) -> None:
        self.vlc_app.small_jump_backwars()

    def grid_su(self) -> None:
        self.vlc_app.volume_up()
        self.vlc_volume_meter.setValue(self.vlc_app.volume())
        self.volume_label.setText(str(round(self.vlc_app.volume() / 2.56)))

    def grid_view_o(self) -> None:
        pass  # Num Page Down
