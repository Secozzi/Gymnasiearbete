from PyQt5.QtCore import QAbstractEventDispatcher, Qt, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QTransform, QFont
from PyQt5.uic import loadUi

# Audio
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Other
import os
import time
from datetime import datetime
from math import ceil

from pyqtkeybind import keybinder
from .key_binder import WinEventFilter
from .widgets import WIDGETS, HomeWidget


CURR_PATH = os.path.dirname(os.path.realpath(__file__))


class InfoThread(QThread):

    time_s = pyqtSignal(str)
    date_s = pyqtSignal(str)
    music = pyqtSignal(str)
    desktop_volume = pyqtSignal(int)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    def run(self):
        while True:
            time_now = datetime.now()
            time.sleep(0.1)
            self.time_s.emit(time_now.strftime("%H:%M:%S"))
            self.date_s.emit(time_now.strftime("V.%V - %a %d %b %Y"))
            self.desktop_volume.emit(round(self.volume.GetMasterVolumeLevelScalar()*100))


class InfoPad(QMainWindow):

    OPACITY_STEP = 0.2

    def __init__(self):
        super().__init__()

        self.menu_grid = self.init_menu_grid(WIDGETS)

        self.current_path = CURR_PATH
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.init_ui()
        self.add_widgets()
        self.start_thread()
        self.show()

    def init_menu_grid(self, apps):
        menu = list(apps)
        while len(menu) < 9:
            menu.append(None)
        return tuple([menu[0:4], menu[5:9]])

    def init_ui(self):
        loadUi(f"{CURR_PATH}/app.ui", self)

        with open(f"{CURR_PATH}/assets/style.qss") as f:
            style_sheet = f.read()
        self.setStyleSheet(style_sheet)

        # Set QPixmaps

        self.scroll_up_arrow.setText("")
        self.scroll_up_arrow.setPixmap(QPixmap(f"{self.current_path}/assets/scroll_bar_arrow.png"))
        self.scroll_up_arrow.setScaledContents(True)

        self.scroll_down_arrow.setText("")
        _upside_down_arrow = QPixmap(f"{self.current_path}/assets/scroll_bar_arrow.png").transformed(QTransform().rotate(180))
        self.scroll_down_arrow.setPixmap(_upside_down_arrow)
        self.scroll_down_arrow.setScaledContents(True)

        self.mic_state_label.setText("")
        self.mic_state_label.setPixmap(QPixmap(f"{self.current_path}/assets/mic_on.png"))
        self.mic_state_label.setScaledContents(True)

        self.desktop_volume.setText("")
        self.desktop_volume.setPixmap(QPixmap(f"{self.current_path}/assets/desktop.png"))
        self.desktop_volume.setScaledContents(True)

        self.desktop_volume_meter.setMinimum(0)
        self.desktop_volume_meter.setMaximum(100)

        self.program_volume_meter.setMinimum(0)
        self.program_volume_meter.setMaximum(100)

    def start_thread(self):
        self.i_thread = InfoThread()
        self.i_thread.time_s.connect(self.update_time)
        self.i_thread.date_s.connect(self.update_date)
        self.i_thread.desktop_volume.connect(self.update_desktop_volume)
        self.i_thread.start()

    def add_widgets(self):
        for widget in [HomeWidget] + list(WIDGETS):
            _widget = widget(self)
            self.stackedWidget.addWidget(_widget)
        self.stackedWidget.setCurrentIndex(0)

    def set_index(self, index):
        self.stackedWidget.setCurrentIndex(index)

    def update_time(self, time_s):
        self.time_string.setText(time_s)

    def update_date(self, date_s):
        self.date_string.setText(date_s)

    def update_desktop_volume(self, d_volume):
        if d_volume == 100:
            self.desktop_volume_label.setFont(QFont("Cascadia Mono", 10))
        else:
            self.desktop_volume_label.setFont(QFont("Cascadia Mono", 18))
        self.desktop_volume_label.setText(str(d_volume))
        self.desktop_volume_meter.setValue(d_volume)

    def grid_1(self):
        self.stackedWidget.currentWidget().grid_1()

    def grid_2(self):
        self.stackedWidget.currentWidget().grid_2()

    def grid_3(self):
        self.stackedWidget.currentWidget().grid_3()

    def grid_4(self):
        self.stackedWidget.currentWidget().grid_4()

    def grid_5(self):
        self.stackedWidget.currentWidget().grid_5()

    def grid_6(self):
        self.stackedWidget.currentWidget().grid_6()

    def grid_7(self):
        self.stackedWidget.currentWidget().grid_7()

    def grid_8(self):
        self.stackedWidget.currentWidget().grid_8()

    def grid_view_o(self):
        print("Viewing overlay")

    def grid_sd(self):
        self.stackedWidget.currentWidget().grid_sd()

    def grid_su(self):
        self.stackedWidget.currentWidget().grid_su()

    def grid_ou(self):
        _opacity = self.windowOpacity()
        if _opacity < 1.0:
            self.setWindowOpacity(_opacity + self.OPACITY_STEP)

    def grid_od(self):
        _opacity = self.windowOpacity()
        if _opacity > 0:
            self.setWindowOpacity(_opacity - self.OPACITY_STEP)

    def grid_mm(self):
        self.stackedWidget.currentWidget().grid_mm()

    def grid_home(self):
        self.stackedWidget.setCurrentIndex(0)


def main():
    import sys

    app = QApplication(sys.argv)

    info_app = InfoPad()

    keybinder.init()
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F13", info_app.grid_sd)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F14", info_app.grid_su)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F15", info_app.grid_view_o)

    keybinder.register_hotkey(info_app.winId(), "Ctrl+F16", info_app.grid_1)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F17", info_app.grid_2)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F18", info_app.grid_3)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F19", info_app.grid_4)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F20", info_app.grid_5)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F21", info_app.grid_6)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F22", info_app.grid_7)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F23", info_app.grid_8)

    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F13", info_app.grid_home)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F14", info_app.grid_ou)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F15", info_app.grid_od)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F16", info_app.grid_mm)

    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
