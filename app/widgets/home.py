from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class HomeWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        loadUi(f"{self.main_window.current_path}/widgets/home.ui", self)

    def grid_1(self):
        self.main_window.set_index(1)

    def grid_2(self):
        self.main_window.set_index(2)

    def grid_3(self):
        print("Activated Num 9 for home")

    def grid_4(self):
        print("Activated Num 4 for home")

    def grid_5(self):
        print("Activated Num 5 for home")

    def grid_6(self):
        print("Activated Num 6 for home")

    def grid_7(self):
        print("Activated Num 1 for home")

    def grid_8(self):
        print("Activated Num 2 for home")

    def grid_9(self):
        print("Activated Num 3 for home")

    def grid_10(self):
        print("Activated Num 0 for home")

    def grid_home(self):
        # Isn't called yet
        print("Activated Num del for home")

    def grid_sd(self):
        print("Activated Num Enter for home")

    def grid_su(self):
        print("Activated Num + for home")

    def grid_vu(self):
        print("Activated Num - for home")

    def grid_vd(self):
        print("Activated num * for home")

    def grid_mm(self):
        print("Activated num / for home")
