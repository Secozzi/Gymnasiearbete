from PyQt5.QtCore import QAbstractEventDispatcher, Qt, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

from pyqtkeybind import keybinder
from key_binder import WinEventFilter
from widgets import HomeWidget

import time
from datetime import datetime

import os
CURR_PATH = os.path.dirname(os.path.realpath(__file__))


class InfoThread(QThread):

    time_s = pyqtSignal(str)
    music = pyqtSignal(str)

    def run(self):
        while True:
            time_now = datetime.now()
            time.sleep(0.1)
            self.time_s.emit(time_now.strftime("%H:%M:%S V.%V %b %d"))


class InfoPad(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_path = CURR_PATH
        #self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.init_ui()
        self.add_widgets()
        self.start_thread()
        self.show()

    def init_ui(self):
        loadUi(f'{CURR_PATH}/assets/app.ui', self)

        with open(f"{CURR_PATH}/assets/style.qss") as f:
            style_sheet = f.read()
        self.setStyleSheet(style_sheet)

    def start_thread(self):
        self.i_thread = InfoThread()
        self.i_thread.time_s.connect(self.update_time)
        self.i_thread.start()

    def add_widgets(self):
        pass
        #home_widget = HomeWidget(self)
        #self.stackedWidget.addWidget(home_widget)

    def update_time(self, time_s):
        #print(time_s)
        self.time_string.setText(time_s)

    def grid_1(self):
        print("Activated Num 7")

    def grid_2(self):
        print("Activated Num 8")

    def grid_3(self):
        print("Activated Num 9")

    def grid_4(self):
        print("Activated Num 4")

    def grid_5(self):
        print("Activated Num 5")

    def grid_6(self):
        print("Activated Num 6")

    def grid_7(self):
        print("Activated Num 1")

    def grid_8(self):
        print("Activated Num 2")

    def grid_9(self):
        print("Activated Num 3")

    def grid_10(self):
        print("Activated Num 0")

    def grid_home(self):
        print("Activated Num del")

    def grid_sd(self):
        print("Activated Num Enter")

    def grid_su(self):
        print("Activated Num +")

    def grid_vu(self):
        print("Activated Num -")

    def grid_vd(self):
        print("Activated num *")

    def grid_mm(self):
        print("Activated num /")


def main():
    import sys
    app = QApplication(sys.argv)

    info_app = InfoPad()

    keybinder.init()
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F13", info_app.grid_1)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F14", info_app.grid_2)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F15", info_app.grid_3)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F16", info_app.grid_4)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F17", info_app.grid_5)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F18", info_app.grid_6)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F19", info_app.grid_7)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F20", info_app.grid_8)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F21", info_app.grid_9)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F22", info_app.grid_10)

    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F13", info_app.grid_home)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F14", info_app.grid_sd)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F15", info_app.grid_su)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F16", info_app.grid_vu)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F17", info_app.grid_vd)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F18", info_app.grid_mm)

    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
