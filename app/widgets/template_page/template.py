from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi


class TemplateWidget(QWidget):

    display_name = "Template"

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        loadUi(f"{self.main_window.current_path}/widgets/template_page/template.ui", self)

    @staticmethod
    def get_icon(curr_path):
        return QPixmap(f"{curr_path}/widgets/template_page/template.png")

    def on_enter(self):
        pass  # Called on enter

    def on_exit(self):
        pass  # Called on exit

    def grid_1(self):
        pass  # Num 4

    def grid_2(self):
        pass  # Num 5

    def grid_3(self):
        pass  # Num 6

    def grid_4(self):
        pass  # Num +

    def grid_5(self):
        pass  # Num 1

    def grid_6(self):
        pass  # Num 2

    def grid_7(self):
        pass  # Num 3

    def grid_8(self):
        pass  # Num Enter

    def grid_9(self):
        pass  # Num 9

    def grid_sd(self):
        pass  # Num 7

    def grid_su(self):
        pass  # Num 8

    def grid_view_o(self):
        pass  # Num Page Down
