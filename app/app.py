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

# PyQt5
from PyQt5.QtCore import QAbstractEventDispatcher, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPixmap, QTransform, QFont
from PyQt5.uic import loadUi
import resources

# Other
from os import path
from math import ceil
from subprocess import Popen
from pyqtkeybind import keybinder

# Relative
from key_binder import WinEventFilter
from widgets import WIDGETS, HomeWidget
from infothread import InfoThread


CURR_PATH = path.dirname(path.realpath(__file__))


class InfoPad(QMainWindow):
    """Main window of application."""

    OPACITY_STEP = 0.2
    NO_OF_APPS = len(WIDGETS)

    def __init__(self, screen_count: int) -> None:
        """Initializes the app"""
        super().__init__()

        self.menu_grid = self.init_menu_grid(WIDGETS)
        self.active_mic = True
        self.scroll_counter = 0

        if screen_count == 3:
            self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.current_path = CURR_PATH
        Popen(
            [
                r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
                f"{self.current_path}/win_func.ahk",
            ]
        )

        self.i_thread = InfoThread()
        self.init_ui()
        self.add_widgets()
        self.start_thread()
        self.update_menu()
        self.show()

    @staticmethod
    def init_menu_grid(apps: tuple) -> tuple:
        """Initialize the menu tuple, only allowing 8 maximum items"""
        menu = list(apps)
        while len(menu) < 9:
            menu.append(None)
        return tuple(menu[0:8])

    def scroll_up(self) -> None:
        """Shifts the menu tuple by 4 steps, if allowed. The first four items
        in the menu tuple will become the last four and the four items before
        the first four items will become the first four items in the menu tuple.

        [] = all applications
        () = the 8 or less applications shown on screen

        Before scrolling up:
        [1, 2, 3, 4, (5, 6, 7, 8, 9, 10, 11, 12), 13]
        After scrolling up:
        [(1, 2, 3, 4, 5, 6, 7, 8), 9, 10, 11, 12, 13]"""
        if self.scroll_counter > 0:
            new_menu = []
            start = (self.scroll_counter - 1) * 4
            to_insert = list(WIDGETS[start : start + 4])

            new_menu += to_insert
            new_menu += self.menu_grid[0:4]
            self.menu_grid = tuple(new_menu)
            self.scroll_counter -= 1

    def scroll_down(self) -> None:
        """Shifts the menu tuple by 4 steps, if allowed. The last four items
        in the menu tuple will become the first four and the four (or less)
        items after the last four items will become the last four items in the
        menu tuple.

        [] = all applications
        () = the 8 or less applications shown on screen

        Before scrolling up:
        [(1, 2, 3, 4, 5, 6, 7, 8), 9, 10, 11, 12, 13]
        After scrolling up:
        [1, 2, 3, 4, (5, 6, 7, 8, 9, 10, 11, 12), 13]
        """
        step = ceil((self.NO_OF_APPS - 8) / 4)
        if self.scroll_counter < step:
            new_menu = []
            next_item = 8 + 4 * self.scroll_counter
            to_insert = list(WIDGETS[next_item : next_item + 4])

            while len(to_insert) < 4:
                to_insert.append(None)

            new_menu += self.menu_grid[4:9]
            new_menu += to_insert
            self.menu_grid = tuple(new_menu)
            self.scroll_counter += 1

    def init_ui(self) -> None:
        """Initialize the UI

        Load from .ui file and apply stylesheet.
        Set QPixmaps on corresponding labels.
        """

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
        self.scroll_up_arrow.setPixmap(
            QPixmap(f"{self.current_path}/assets/scroll_bar_arrow.png")
        )
        self.scroll_up_arrow.setScaledContents(True)

        self.scroll_down_arrow.setText("")
        _upside_down_arrow = QPixmap(
            f"{self.current_path}/assets/scroll_bar_arrow.png"
        ).transformed(QTransform().rotate(180))
        self.scroll_down_arrow.setPixmap(_upside_down_arrow)
        self.scroll_down_arrow.setScaledContents(True)

        self.mic_state_label.setText("")
        self.mic_state_label.setPixmap(
            QPixmap(f"{self.current_path}/assets/mic_on.png")
        )
        self.mic_state_label.setScaledContents(True)

        self.desktop_volume.setText("")
        self.desktop_volume.setPixmap(
            QPixmap(f"{self.current_path}/assets/desktop.png")
        )
        self.desktop_volume.setScaledContents(True)

        # Initialize sliders
        self.desktop_volume_meter.setMinimum(0)
        self.desktop_volume_meter.setMaximum(100)

    def update_menu(self) -> None:
        """Updates menu.

        Gets index of first and last widget viewed on screen and total amount of widgets.
        Updates text and icon on each grid index.
        """
        self.first_menu_label.setText(str(WIDGETS.index(self.menu_grid[0]) + 1))
        self.last_menu_label.setText(
            str(WIDGETS.index(list(filter(None.__ne__, self.menu_grid))[-1]) + 1)
        )
        self.total_menu_label.setText(str(self.NO_OF_APPS))

        home_widget = self.stackedWidget.currentWidget()
        for index, app in enumerate(self.menu_grid):
            if app:
                getattr(home_widget, f"icon_{index}").setText("")
                getattr(home_widget, f"icon_{index}").setPixmap(
                    app.get_icon(self.current_path)
                )
                getattr(home_widget, f"icon_{index}").setScaledContents(True)
                getattr(home_widget, f"text_{index}").setText(app.display_name)
            else:
                getattr(home_widget, f"icon_{index}").clear()
                getattr(home_widget, f"text_{index}").clear()

    def start_thread(self) -> None:
        """Connect signals to each respective function and start thread"""
        self.i_thread.time_s.connect(self.update_time)
        self.i_thread.date_s.connect(self.update_date)
        self.i_thread.desktop_volume.connect(self.update_desktop_volume)
        self.i_thread.music.connect(self.update_music)
        self.i_thread.start()

    def add_widgets(self) -> None:
        """Create instances of each widget and add it to the stacked widget"""
        for widget in [HomeWidget] + list(WIDGETS):
            _widget = widget(self)
            self.stackedWidget.addWidget(_widget)
        self.stackedWidget.setCurrentIndex(0)

    def set_index(self, index: int) -> None:
        """Sets index on stack widget"""
        self.stackedWidget.setCurrentIndex(index)

    def update_time(self, time_s: str) -> None:
        """Update time label"""
        self.time_string.setText(time_s)

    def update_date(self, date_s: str) -> None:
        """Update date label"""
        self.date_string.setText(date_s)

    def update_desktop_volume(self, d_volume: int) -> None:
        """Update desktop volume slider and label"""
        if d_volume == 100:
            self.desktop_volume_label.setFont(QFont("Cascadia Mono", 10))
        else:
            self.desktop_volume_label.setFont(QFont("Cascadia Mono", 18))
        self.desktop_volume_label.setText(str(d_volume))
        self.desktop_volume_meter.setValue(d_volume)

    def update_music(self, playback: str) -> None:
        """Update label showing current spotify playback information"""
        self.music_string.setText(playback)

    def grid_1(self) -> None:
        self.stackedWidget.currentWidget().grid_1()

    def grid_2(self) -> None:
        self.stackedWidget.currentWidget().grid_2()

    def grid_3(self) -> None:
        self.stackedWidget.currentWidget().grid_3()

    def grid_4(self) -> None:
        self.stackedWidget.currentWidget().grid_4()

    def grid_5(self) -> None:
        self.stackedWidget.currentWidget().grid_5()

    def grid_6(self) -> None:
        self.stackedWidget.currentWidget().grid_6()

    def grid_7(self) -> None:
        self.stackedWidget.currentWidget().grid_7()

    def grid_8(self) -> None:
        self.stackedWidget.currentWidget().grid_8()

    def grid_9(self) -> None:
        self.stackedWidget.currentWidget().grid_9()

    def grid_sd(self) -> None:
        self.stackedWidget.currentWidget().grid_sd()

    def grid_su(self) -> None:
        self.stackedWidget.currentWidget().grid_su()

    def grid_ou(self) -> None:
        """Turn up opacity on window"""
        _opacity = self.windowOpacity()
        if _opacity < 1.0:
            self.setWindowOpacity(_opacity + self.OPACITY_STEP)

    def grid_od(self) -> None:
        """Turn down opacity on window"""
        _opacity = self.windowOpacity()
        if _opacity > 0:
            self.setWindowOpacity(_opacity - self.OPACITY_STEP)

    def grid_view_o(self) -> None:
        """Refresh spotify PID on info thread"""
        self.i_thread.refresh_spotify()

    def grid_mm(self) -> None:
        """Toggle mic picture state"""
        if self.active_mic:
            self.mic_state_label.setPixmap(
                QPixmap(f"{self.current_path}/assets/mic_off.png")
            )
            self.active_mic = False
        else:
            self.mic_state_label.setPixmap(
                QPixmap(f"{self.current_path}/assets/mic_on.png")
            )
            self.active_mic = True

    def grid_home(self) -> None:
        """Call on_exit() method on top widget and go to the home screen"""
        self.stackedWidget.currentWidget().on_exit()
        self.stackedWidget.setCurrentIndex(0)
        self.update_menu()


def main() -> None:
    import sys

    app = QApplication(sys.argv)
    screen_count = QDesktopWidget().screenCount()

    info_app = InfoPad(screen_count)

    # Register hotkeys
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

    # Install native event filter
    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    # If three monitors detected, move window to thirds screen and make it fullscreen
    if screen_count == 3:
        monitor = QDesktopWidget().screenGeometry(2)
        info_app.move(monitor.left(), monitor.top())
        info_app.showFullScreen()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
