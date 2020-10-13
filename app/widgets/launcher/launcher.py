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

from subprocess import Popen
from math import ceil
import re as pyreg
import json


class LauncherWidget(QWidget):
    """Widget for the launcher application. It displays
    every application in a 2x4 grid that the user can
    scroll up and down. Every application has its own
    icon and display name.

    The data is stored in "data.json" as a list. Each element
    is a list with [display_name, path_to_exe,
    name_for_icon_in_icon_folder.png]. Path to exe is the full
    path to the exe. In order to launch steam games, the full
    path is replaced by steam://{id} where id is the app id.

    Constants:
    display_name - str
        Display name for application
    icons_path - str
        Relative path to the icons folder, base path is the
        current path from the app.pyw containing the main
        window. This application will search in this folder
        for the name of the image given by the data.json file.
    steam_path - str
        Full path to steam.exe.
    """

    display_name = "Appar"
    icons_path = "/widgets/launcher/icons"
    steam_path = r"F:\Program Files (x86)\Steam\Steam.exe"

    def __init__(self, main_window: 'InfoPad') -> None:
        super().__init__()
        self.main_window = main_window
        self.icons_path = self.main_window.current_path + self.icons_path

        self.launcher_data = {}
        self.launch_index = []
        self.no_of_apps = 0
        self.scroll_counter = 0

        # load data.json file and initialize some variables
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
            to_insert = list(self.launcher_data[start:start + 4])

            new_menu += to_insert
            new_menu += self.apps_grid[0:4]
            self.apps_grid = tuple(new_menu)
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
        """Set labels of the scroll bar to correct value.
        Reset scroll counter and update the menu."""
        self.main_window.total_menu_label.setText(str(self.no_of_apps))

        if self.no_of_apps < 8:
            self.main_window.last_menu_label.setText(str(self.no_of_apps))
        else:
            self.main_window.last_menu_label.setText("8")

        self.scroll_counter = 0
        self.update_menu()

    def update_menu(self) -> None:
        """Updates menu.

        Gets index of first and last widget viewed on screen and total amount of widgets.
        Updates text and icon on each grid index.
        """
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
        """Launches the app by executing the command in a
        new process. A regex is performed in order to check
        if 'steam://{some_id}' is presend and if so, launch
        "{steam_path} -applaunch some_id" instead of the
        path given.

        :param path: str
            Full path of the executable or steam://{app_id}.
        """
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
