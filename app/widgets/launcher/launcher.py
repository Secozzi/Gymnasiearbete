from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

from subprocess import Popen
from math import ceil
import re as pyreg
import json


class LauncherWidget(QWidget):

    display_name = "Appar"
    icons_path = "/widgets/launcher/icons"
    steam_path = r"F:\Program Files (x86)\Steam\Steam.exe"

    def __init__(self, main_window) -> None:
        super().__init__()
        self.main_window = main_window
        self.icons_path = self.main_window.current_path + self.icons_path

        self.launcher_data = {}
        self.launch_index = []
        self.no_of_apps = 0
        self.scroll_counter = 0

        with open(f"{self.main_window.current_path}/widgets/launcher/data.json") as f:
            self.launcher_data = tuple(json.load(f))

        self.no_of_apps = len(self.launcher_data)

        self.apps_grid = self.init_app_menu(self.launcher_data)

        loadUi(f"{self.main_window.current_path}/widgets/launcher/launcher.ui", self)

    @staticmethod
    def get_icon(curr_path: str) -> QPixmap:
        return QPixmap(f"{curr_path}/widgets/launcher/launcher.png")

    @staticmethod
    def init_app_menu(apps: tuple) -> tuple:
        menu = list(apps)
        while len(menu) < 9:
            menu.append(None)
        return tuple(menu[0:8])

    def scroll_up(self) -> None:
        if self.scroll_counter > 0:
            new_menu = []
            start = (self.scroll_counter - 1) * 4
            to_insert = list(self.launcher_data[start:start + 4])

            new_menu += to_insert
            new_menu += self.apps_grid[0:4]
            self.apps_grid = tuple(new_menu)
            self.scroll_counter -= 1

    def scroll_down(self) -> None:
        step = ceil((len(self.launcher_data) - 8) / 4)
        if self.scroll_counter < step:
            new_menu = []
            next_item = 8 + 4 * self.scroll_counter
            to_insert = list(self.launcher_data[next_item:next_item + 4])

            while len(to_insert) < 4:
                to_insert.append(None)

            new_menu += self.apps_grid[4:9]
            new_menu += to_insert
            self.apps_grid = tuple(new_menu)
            self.scroll_counter += 1

    def on_enter(self) -> None:
        self.main_window.total_menu_label.setText(str(self.no_of_apps))

        if self.no_of_apps < 8:
            self.main_window.last_menu_label.setText(str(self.no_of_apps))
        else:
            self.main_window.last_menu_label.setText("8")

        self.scroll_counter = 0
        self.update_menu()

    def update_menu(self) -> None:
        self.main_window.first_menu_label.setText(str(self.launcher_data.index(self.apps_grid[0]) + 1))
        self.main_window.last_menu_label.setText(str(self.launcher_data.index(list(filter(None.__ne__, self.apps_grid))[-1]) + 1))
        self.main_window.total_menu_label.setText(str(self.no_of_apps))

        home_widget = self.main_window.stackedWidget.currentWidget()
        for index, app_info in enumerate(self.apps_grid):
            if app_info:
                getattr(home_widget, f"text_{index}").setText(app_info[0])
                _pixmap = QPixmap(f"{self.icons_path}/{app_info[2]}")
                getattr(home_widget, f"icon_{index}").setText("")
                getattr(home_widget, f"icon_{index}").setPixmap(_pixmap)
            else:
                getattr(home_widget, f"text_{index}").setText("")
                getattr(home_widget, f"icon_{index}").setText("")
                getattr(home_widget, f"icon_{index}").clear()

    def on_exit(self) -> None:
        pass

    def launch_app(self, path: str) -> None:
        regex = pyreg.compile(r"steam:\/\/([0-z]+)")
        m = regex.search(path)

        if m:
            Popen(f"{self.steam_path} -applaunch {m.group(1)}")
        else:
            Popen(path)

    def grid_1(self) -> None:
        self.launch_app(self.launcher_data[self.scroll_counter * 4][1])

    def grid_2(self) -> None:
        if self.no_of_apps >= 2 + self.scroll_counter * 4:
            self.launch_app(self.launcher_data[1 + self.scroll_counter * 4][1])

    def grid_3(self) -> None:
        if self.no_of_apps >= 3 + self.scroll_counter * 4:
            self.launch_app(self.launcher_data[2 + self.scroll_counter * 4][1])

    def grid_4(self) -> None:
        if self.no_of_apps >= 4 + self.scroll_counter * 4:
            self.launch_app(self.launcher_data[3 + self.scroll_counter * 4][1])

    def grid_5(self) -> None:
        if self.no_of_apps >= 5 + self.scroll_counter * 4:
            self.launch_app(self.launcher_data[4 + self.scroll_counter * 4][1])

    def grid_6(self) -> None:
        if self.no_of_apps >= 6 + self.scroll_counter * 4:
            self.launch_app(self.launcher_data[5 + self.scroll_counter * 4][1])

    def grid_7(self) -> None:
        if self.no_of_apps >= 7 + self.scroll_counter * 4:
            self.launch_app(self.launcher_data[6 + self.scroll_counter * 4][1])

    def grid_8(self) -> None:
        if self.no_of_apps >= 8 + self.scroll_counter * 4:
            self.launch_app(self.launcher_data[7 + self.scroll_counter * 4][1])

    def grid_9(self) -> None:
        pass  # Num 9

    def grid_sd(self) -> None:
        self.scroll_down()
        self.update_menu()

    def grid_su(self) -> None:
        self.scroll_up()
        self.update_menu()

    def grid_view_o(self) -> None:
        pass  # Num Page Down
