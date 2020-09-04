from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class HomeWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        loadUi(f"{self.main_window.current_path}/widgets/home.ui")