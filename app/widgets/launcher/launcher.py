from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import json
from math import ceil


class LauncherWidget(QWidget):

    display_name = "Appar"
    steam_path = r"F:\Program Files (x86)\Steam\Steam.exe"

    def __init__(self, main_window) -> None:
        super().__init__()
        self.main_window = main_window
        self.launcher_data = {}
        self.launch_index = []
        self.scroll_counter = 0

        loadUi(f"{self.main_window.current_path}/widgets/launcher/launcher.ui", self)

    @staticmethod
    def get_icon(curr_path: str) -> QPixmap:
        return QPixmap(f"{curr_path}/widgets/launcher/launcher.png")

    def scroll_up(self) -> None:
        if self.scroll_counter > 0:
            new_menu = []
            start = (self.scroll_counter - 1) * 4
            to_insert = list(self.launcher_data[start:start + 4])

            new_menu += to_insert
            new_menu += self.menu_grid[0:4]
            self.launcher_data = tuple(new_menu)
            self.scroll_counter -= 1

    def scroll_down(self) -> None:
        step = ceil((len(self.launcher_data) - 8) / 4)
        if self.scroll_counter < step:
            new_menu = []
            next_item = 8 + 4 * self.scroll_counter
            to_insert = list(self.launcher_data[next_item:next_item + 4])

            while len(to_insert) < 4:
                to_insert.append(None)

            new_menu += self.menu_grid[4:9]
            new_menu += to_insert
            self.launcher_data = tuple(new_menu)
            self.scroll_counter += 1

    def on_enter(self) -> None:
        with open(f"{self.main_window.current_path}/widgets/launcher/data.json") as f:
            self.launcher_data = tuple(json.load(f))

        print(self.launcher_data)
        print(type(self.launcher_data))

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
