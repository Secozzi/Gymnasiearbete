from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

import subprocess


class VLCWidget(QWidget):
    """
    Control a vlc instance with global shortcuts. Shortcuts:

    Pause/Play      - Ctrl + Alt + Shift + 1 - Num 5
    Volume up       - Ctrl + Alt + Shift + 2 - Num +
    Volume down     - Ctrl + Alt + Shift + 3 - Num E
    Back 10 sec     - Ctrl + Alt + Shift + 4 - Num 7
    Forward 10 sec  - Ctrl + Alt + Shift + 5 - Num 9
    Back 1 min      - Ctrl + Alt + Shift + 6 - Num 1
    Forward 1 min   - Ctrl + Alt + Shift + 7 - Num 3
    Next track      - Ctrl + Alt + Shift + 8 - Num 6
    Previous track  - Ctrl + Alt + Shift + 9 - Num 4
    """

    display_name = "Vlc"

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        loadUi(f"{self.main_window.current_path}/widgets/vlc/vlc.ui", self)

    @staticmethod
    def get_icon(curr_path):
        return QPixmap(f"{curr_path}/widgets/vlc/vlc.png")

    def on_enter(self):
        pass  # Called on enter

    def on_exit(self):
        pass  # Called on exit

    def grid_1(self):
        subprocess.call([r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
                         f"{self.main_window.current_path}/widgets/vlc/pt.ahk"])

    def grid_2(self):
        subprocess.call([r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
                         f"{self.main_window.current_path}/widgets/vlc/play.ahk"])

    def grid_3(self):
        subprocess.call([r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
                         f"{self.main_window.current_path}/widgets/vlc/nt.ahk"])

    def grid_4(self):
        subprocess.call([r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
                         f"{self.main_window.current_path}/widgets/vlc/vup.ahk"])

    def grid_5(self):
        subprocess.call([r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
                         f"{self.main_window.current_path}/widgets/vlc/b1m.ahk"])

    def grid_6(self):
        pass  # Num 2

    def grid_7(self):
        subprocess.call([r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
                         f"{self.main_window.current_path}/widgets/vlc/f1m.ahk"])

    def grid_8(self):
        subprocess.call([r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
                         f"{self.main_window.current_path}/widgets/vlc/vud.ahk"])

    def grid_9(self):
        subprocess.call([r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
                         f"{self.main_window.current_path}/widgets/vlc/f10s.ahk"])

    def grid_sd(self):
        subprocess.call([r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
                         f"{self.main_window.current_path}/widgets/vlc/b10s.ahk"])

    def grid_su(self):
        pass  # Num 8

    def grid_view_o(self):
        pass  # Num Page Down
