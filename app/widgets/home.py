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
from PyQt5.uic import loadUi


class HomeWidget(QWidget):
    """Home screen of app. It displays every application in
    a 2x4 grid that the user can scroll up and down. Every
    application has its own icon and display name"""

    def __init__(self, main_window: "InfoPad") -> None:
        super().__init__()
        self.main_window = main_window

        loadUi(f"{self.main_window.current_path}/widgets/home.ui", self)

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    def grid_1(self) -> None:
        self.main_window.set_index(1 + self.main_window.scroll_counter * 4)
        self.main_window.stackedWidget.currentWidget().on_enter()

    def grid_2(self) -> None:
        if self.main_window.NO_OF_APPS >= 2 + self.main_window.scroll_counter * 4:
            self.main_window.set_index(2 + self.main_window.scroll_counter * 4)
            self.main_window.stackedWidget.currentWidget().on_enter()

    def grid_3(self) -> None:
        if self.main_window.NO_OF_APPS >= 3 + self.main_window.scroll_counter * 4:
            self.main_window.set_index(3 + self.main_window.scroll_counter * 4)
            self.main_window.stackedWidget.currentWidget().on_enter()

    def grid_4(self) -> None:
        if self.main_window.NO_OF_APPS >= 4 + self.main_window.scroll_counter * 4:
            self.main_window.set_index(4 + self.main_window.scroll_counter * 4)
            self.main_window.stackedWidget.currentWidget().on_enter()

    def grid_5(self) -> None:
        if self.main_window.NO_OF_APPS >= 5 + self.main_window.scroll_counter * 4:
            self.main_window.set_index(5 + self.main_window.scroll_counter * 4)
            self.main_window.stackedWidget.currentWidget().on_enter()

    def grid_6(self) -> None:
        if self.main_window.NO_OF_APPS >= 6 + self.main_window.scroll_counter * 4:
            self.main_window.set_index(6 + self.main_window.scroll_counter * 4)
            self.main_window.stackedWidget.currentWidget().on_enter()

    def grid_7(self) -> None:
        if self.main_window.NO_OF_APPS >= 7 + self.main_window.scroll_counter * 4:
            self.main_window.set_index(7 + self.main_window.scroll_counter * 4)
            self.main_window.stackedWidget.currentWidget().on_enter()

    def grid_8(self) -> None:
        if self.main_window.NO_OF_APPS >= 8 + self.main_window.scroll_counter * 4:
            self.main_window.set_index(8 + self.main_window.scroll_counter * 4)
            self.main_window.stackedWidget.currentWidget().on_enter()

    def grid_9(self) -> None:
        pass
        # self.main_window.showFullScreen()

    def grid_sd(self) -> None:
        self.main_window.scroll_down()
        self.main_window.update_menu()

    def grid_su(self) -> None:
        self.main_window.scroll_up()
        self.main_window.update_menu()
