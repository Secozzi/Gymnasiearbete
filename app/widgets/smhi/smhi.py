from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi


class SmhiWidget(QWidget):

    display_name = "Väder"

    def __init__(self, main_window) -> None:
        super().__init__()
        self.main_window = main_window

        loadUi(f"{self.main_window.current_path}/widgets/smhi/smhi.ui", self)

    @staticmethod
    def get_icon(curr_path: str) -> QPixmap:
        return QPixmap(f"{curr_path}/widgets/smhi/smhi.png")

    def on_enter(self) -> None:
        pass  # Called on enter

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
