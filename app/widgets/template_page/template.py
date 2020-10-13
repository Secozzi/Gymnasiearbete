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


class TemplateWidget(QWidget):
    """This is a template page that contains all necessary methods
    in order to create a working application.

    template.png is the icon used to display the application on the home screen.
    template.py is the file containing the widget.
    template.ui is the "Qt Designer User Interface" file loaded.

    disaply_name is the name shown on the home screen.
    """

    display_name = "Template"

    def __init__(self, main_window: 'InfoPad') -> None:
        """Initialize the widget, super it, pass
        instance of the main window, and load the UI file"""
        super().__init__()
        self.main_window = main_window

        loadUi(f"{self.main_window.current_path}/widgets/template_page/template.ui", self)

    @staticmethod
    def get_icon(curr_path: str) -> QPixmap:
        """This methods gets called when the home screen will display the application.

        :param curr_path: str
            The current path of this python project. curr_path is based on app.pyw, the main
            window file.
        :return: QPixmap
            Returns a QPixmap object of the image.
        """
        return QPixmap(f"{curr_path}/widgets/template_page/template.png")

    def on_enter(self) -> None:
        """This method gets called every time the user enters this application"""
        pass

    def on_exit(self) -> None:
        """This method gets called after the user goes back to the home screen"""
        pass

    def grid_1(self) -> None:
        """The method called when the user presses 'grid 1'.
        This corresponds to 'num 0 + num 4'"""
        pass

    def grid_2(self) -> None:
        """The method called when the user presses 'grid 2'.
        This corresponds to 'num 0 + num 5'"""
        pass

    def grid_3(self) -> None:
        """The method called when the user presses 'grid 3'.
        This corresponds to 'num 0 + num 6'"""
        pass

    def grid_4(self) -> None:
        """The method called when the user presses 'grid 4'.
        This corresponds to 'num 0 + num +'"""
        pass

    def grid_5(self) -> None:
        """The method called when the user presses 'grid 5'.
        This corresponds to 'num 0 + num 1'"""
        pass

    def grid_6(self) -> None:
        """The method called when the user presses 'grid 6'.
        This corresponds to 'num 0 + num 2'"""
        pass

    def grid_7(self) -> None:
        """The method called when the user presses 'grid 7'.
        This corresponds to 'num 0 + num 3'"""
        pass

    def grid_8(self) -> None:
        """The method called when the user presses 'grid 8'.
        This corresponds to 'num 0 + num enter'"""
        pass

    def grid_9(self) -> None:
        """The method called when the user presses 'grid 9'.
        This corresponds to 'num 0 + num 9'"""
        pass

    def grid_sd(self) -> None:
        """The method called when the user presses 'grid scroll down'.
        This corresponds to 'num 0 + num 7'"""
        pass

    def grid_su(self) -> None:
        """The method called when the user presses 'grid scroll up'.
        This corresponds to 'num 0 + num 8'"""
        pass

    def grid_view_o(self) -> None:
        """The method called when the user presses 'grid view overlay'.
        This corresponds to 'num 0 + page down'

        Note: as of current, this method will never get called
        """
        pass
