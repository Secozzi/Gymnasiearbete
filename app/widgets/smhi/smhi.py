from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

from .data_thread import SmhiThread
from pprint import pprint


class SmhiWidget(QWidget):

    display_name = "Väder"

    def __init__(self, main_window) -> None:
        super().__init__()
        self.main_window = main_window
        self.data_thead = SmhiThread()

        loadUi(f"{self.main_window.current_path}/widgets/smhi/smhi.ui", self)

    @staticmethod
    def get_icon(curr_path: str) -> QPixmap:
        return QPixmap(f"{curr_path}/widgets/smhi/smhi.png")

    def update_ui(self, input_dict) -> None:
        smhi_widget = self.main_window.stackedWidget.currentWidget()

        for key in list(input_dict.keys()):
            params = input_dict[key]
            getattr(smhi_widget, f"time_{key}").setText(params[0])
            getattr(smhi_widget, f"info_{key}").setText(f"{params[1]}°C - {params[2]}mm")
            _pixmap = QPixmap(f"{self.main_window.current_path}/widgets/smhi/icons/{params[3]}.png")
            getattr(smhi_widget, f"icon_{key}").setPixmap(_pixmap)

    def on_enter(self) -> None:
        self.data_thead.weather_info.connect(self.update_ui)
        self.data_thead.start()

    def on_exit(self) -> None:
        pass  # Called on exit

    def grid_1(self) -> None:
        pass  # Num 4

    def grid_2(self) -> None:
        pass  # Num 5

    def grid_3(self) -> None:
        pass  # Num 6

    def grid_4(self) -> None:
        pass  # Num +

    def grid_5(self) -> None:
        pass  # Num 1

    def grid_6(self) -> None:
        pass  # Num 2

    def grid_7(self) -> None:
        pass  # Num 3

    def grid_8(self) -> None:
        pass  # Num Enter

    def grid_9(self) -> None:
        pass  # Num 9

    def grid_sd(self) -> None:
        pass  # Num 7

    def grid_su(self) -> None:
        pass  # Num 8

    def grid_view_o(self) -> None:
        pass  # Num Page Down
