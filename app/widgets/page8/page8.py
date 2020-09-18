from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi


class Page8Widget(QWidget):

    display_name = "Page 8"

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        loadUi(f"{self.main_window.current_path}/widgets/page8/page8.ui", self)

    @staticmethod
    def get_icon(curr_path):
        return QPixmap(f"{curr_path}/widgets/page8/page8.png")

    def grid_1(self):
        print("Activated Num 7 for page8")

    def grid_2(self):
        print("Activated Num 8 for page8")

    def grid_3(self):
        print("Activated Num 9 for page8")

    def grid_4(self):
        print("Activated Num 4 for page8")

    def grid_5(self):
        print("Activated Num 5 for page8")

    def grid_6(self):
        print("Activated Num 6 for page8")

    def grid_7(self):
        print("Activated Num 1 for page8")

    def grid_8(self):
        print("Activated Num 2 for page8")

    def grid_9(self):
        print("Activated Num 3 for page8")

    def grid_10(self):
        print("Activated Num 0 for page8")

    def grid_sd(self):
        print("Activated Num Enter for page8")

    def grid_su(self):
        print("Activated Num + for page8")
