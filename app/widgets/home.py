from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class HomeWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        loadUi(f"{self.main_window.current_path}/widgets/home.ui", self)

    def grid_1(self):
        self.main_window.set_index(1 + self.main_window.scroll_counter * 4)

    def grid_2(self):
        if self.main_window.NO_OF_APPS >= 2:
            self.main_window.set_index(2 + self.main_window.scroll_counter * 4)

    def grid_3(self):
        if self.main_window.NO_OF_APPS >= 3:
            self.main_window.set_index(3 + self.main_window.scroll_counter * 4)

    def grid_4(self):
        if self.main_window.NO_OF_APPS >= 4:
            self.main_window.set_index(4 + self.main_window.scroll_counter * 4)

    def grid_5(self):
        if self.main_window.NO_OF_APPS >= 5:
            self.main_window.set_index(5 + self.main_window.scroll_counter * 4)

    def grid_6(self):
        if self.main_window.NO_OF_APPS >= 6:
            self.main_window.set_index(6 + self.main_window.scroll_counter * 4)

    def grid_7(self):
        if self.main_window.NO_OF_APPS >= 7:
            self.main_window.set_index(7 + self.main_window.scroll_counter * 4)

    def grid_8(self):
        if self.main_window.NO_OF_APPS >= 8:
            self.main_window.set_index(8 + self.main_window.scroll_counter * 4)

    def grid_sd(self):
        self.main_window.scroll_down()
        self.main_window.update_menu()

    def grid_su(self):
        self.main_window.scroll_up()
        self.main_window.update_menu()

    def grid_vu(self):
        print("Activated Num - for home")

    def grid_vd(self):
        print("Activated num * for home")

    def grid_mm(self):
        print("Activated num / for home")
