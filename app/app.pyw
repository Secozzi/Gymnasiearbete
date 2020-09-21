from PyQt5.QtCore import QAbstractEventDispatcher, Qt, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QTransform, QFont
from PyQt5.uic import loadUi

# Audio
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Other
from os import path
from time import sleep
from datetime import datetime
from math import ceil
from pyqtkeybind import keybinder

# Spotipy
from configparser import ConfigParser
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Relative
from .key_binder import WinEventFilter
from .widgets import WIDGETS, HomeWidget


CURR_PATH = path.dirname(path.realpath(__file__))
DEVICES = AudioUtilities.GetSpeakers()
INTERFACE = DEVICES.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
VOLUME = cast(INTERFACE, POINTER(IAudioEndpointVolume))

credentials = ConfigParser()
credentials.read(f"{CURR_PATH}/credentials.cfg")

client_id = credentials["SPOTIPY"]["CLIENT_ID"]
client_secret = credentials["SPOTIPY"]["CLIENT_SECRET"]
redirect_uri = credentials["SPOTIPY"]["REDIRECT_URI"]

scope = "user-read-playback-state"
sp = Spotify(client_credentials_manager=SpotifyOAuth(client_id=client_id,
                                                     client_secret=client_secret,
                                                     redirect_uri=redirect_uri,
                                                     cache_path=f"{CURR_PATH}/.cache",
                                                     scope=scope))


class InfoThread(QThread):

    time_s = pyqtSignal(str)
    date_s = pyqtSignal(str)
    music = pyqtSignal(str)
    desktop_volume = pyqtSignal(int)

    REFRESH_REATE = 0.2

    def run(self):

        self.music_length = 22

        while True:
            _master_volume = VOLUME.GetMasterVolumeLevelScalar() * 100
            time_now = datetime.now()

            spotify_info = self.get_spotify_information()

            self.time_s.emit(time_now.strftime("%H:%M:%S"))
            self.date_s.emit(time_now.strftime("V.%V - %a %d %b %Y"))
            self.desktop_volume.emit(round(_master_volume))
            self.music.emit(spotify_info)

            sleep(self.REFRESH_REATE)

    def get_spotify_information(self):
        res = sp.current_playback()

        if res:
            current = self.get_length(res["progress_ms"])
            duration = self.get_length(res["item"]["duration_ms"])

            song_name = res["item"]["name"]

            return f"{current}/{duration} {song_name}"[:self.music_length]
        else:
            return "Nothing playing currently"[:self.music_length]

    def get_length(self, ms):
        s = round(ms / 1000)
        return f"{(s // 60):02d}:{(s % 60):02d}"


class InfoPad(QMainWindow):

    OPACITY_STEP = 0.2
    NO_OF_APPS = len(WIDGETS)

    def __init__(self):
        super().__init__()

        self.menu_grid = self.init_menu_grid(WIDGETS)
        self.active_mic = True
        self.scroll_counter = 0

        self.current_path = CURR_PATH
        #self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.init_ui()
        self.add_widgets()
        self.start_thread()
        self.update_menu()
        self.show()

    def init_menu_grid(self, apps):
        menu = list(apps)
        while len(menu) < 9:
            menu.append(None)
        return tuple(menu[0:8])

    def scroll_up(self):
        if self.scroll_counter > 0:
            new_menu = []
            start = (self.scroll_counter - 1) * 4
            to_insert = list(WIDGETS[start:start + 4])

            new_menu += to_insert
            new_menu += self.menu_grid[0:4]
            self.menu_grid = tuple(new_menu)
            self.scroll_counter -= 1

    def scroll_down(self):
        step = ceil((self.NO_OF_APPS - 8) / 4)
        if self.scroll_counter < step:
            new_menu = []
            next_item = 8 + 4 * self.scroll_counter
            to_insert = list(WIDGETS[next_item:next_item + 4])

            while len(to_insert) < 4:
                to_insert.append(None)

            new_menu += self.menu_grid[4:9]
            new_menu += to_insert
            self.menu_grid = tuple(new_menu)
            self.scroll_counter += 1

    def init_ui(self):
        loadUi(f"{CURR_PATH}/app.ui", self)

        with open(f"{CURR_PATH}/assets/style.qss") as f:
            style_sheet = f.read()
        self.setStyleSheet(style_sheet)

        self.total_menu_label.setText(str(self.NO_OF_APPS))
        if self.NO_OF_APPS < 8:
            self.last_menu_label.setText(str(self.NO_OF_APPS))
        else:
            self.last_menu_label.setText("8")

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

    def update_menu(self):
        self.first_menu_label.setText(str(WIDGETS.index(self.menu_grid[0]) + 1))
        self.last_menu_label.setText(str(WIDGETS.index(list(filter(None.__ne__, self.menu_grid))[-1]) + 1))

        for index, app in enumerate(self.menu_grid):
            if app:
                home_widget = self.stackedWidget.currentWidget()
                getattr(home_widget, f"icon_{index}").setText("")
                getattr(home_widget, f"icon_{index}").setPixmap(app.get_icon(self.current_path))
                getattr(home_widget, f"icon_{index}").setScaledContents(True)
                getattr(home_widget, f"text_{index}").setText(app.display_name)
            else:
                getattr(home_widget, f"icon_{index}").clear()
                getattr(home_widget, f"text_{index}").clear()

    def start_thread(self):
        self.i_thread = InfoThread()
        self.i_thread.time_s.connect(self.update_time)
        self.i_thread.date_s.connect(self.update_date)
        self.i_thread.desktop_volume.connect(self.update_desktop_volume)
        self.i_thread.music.connect(self.update_music)
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

    def update_music(self, playback):
        self.music_string.setText(playback)

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

    def grid_9(self):
        self.stackedWidget.currentWidget().grid_9()

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

    def grid_view_o(self):
        self.stackedWidget.currentWidget().grid_view_o()

    def grid_mm(self):
        if self.active_mic:
            self.mic_state_label.setPixmap(QPixmap(f"{self.current_path}/assets/mic_off.png"))
            self.active_mic = False
        else:
            self.mic_state_label.setPixmap(QPixmap(f"{self.current_path}/assets/mic_on.png"))
            self.active_mic = True

    def grid_home(self):
        self.stackedWidget.currentWidget().on_exit()
        self.stackedWidget.setCurrentIndex(0)
        self.update_menu()


def main():
    import sys

    app = QApplication(sys.argv)

    info_app = InfoPad()

    keybinder.init()
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F13", info_app.grid_sd)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F14", info_app.grid_su)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F15", info_app.grid_9)

    keybinder.register_hotkey(info_app.winId(), "Ctrl+F16", info_app.grid_1)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F17", info_app.grid_2)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F18", info_app.grid_3)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F19", info_app.grid_4)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F20", info_app.grid_5)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F21", info_app.grid_6)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F22", info_app.grid_7)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F23", info_app.grid_8)

    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F13", info_app.grid_home)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F14", info_app.grid_mm)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F15", info_app.grid_ou)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F16", info_app.grid_od)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+Alt+F17", info_app.grid_view_o)

    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
