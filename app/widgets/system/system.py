from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

from .system_thread import SystemThread


class SystemWidget(QWidget):
    """Weather application using the SMHI API. It shows the
    temperature, general weather as an icon, and precipitation
    for the next 24h in a 4x6 grid."""

    display_name = "System"

    def __init__(self, main_window: 'InfoPad') -> None:
        super().__init__()
        self.main_window = main_window
        self.system_thread = SystemThread()

        loadUi(f"{self.main_window.current_path}/widgets/system/system.ui", self)

    @staticmethod
    def get_icon(curr_path: str) -> QPixmap:
        return QPixmap(f"{curr_path}/widgets/system/system.png")

    def on_enter(self) -> None:
        self.system_thread.system_info.connect(self.update_ui)
        self.system_thread.start()

    def on_exit(self) -> None:
        """This method gets called after the user goes back to the home screen"""
        pass

    def update_ui(self, info_list):
        """Updates UI

        :param info_list: list
            [gpu_load, gpu_temp, cpu_load, cpu_temp, mem_usage, ethernet_usage]
        """
        self.gpu_load.setText(f"GPU Load - {info_list[0]}%")
        self.gpu_temp.setText(f"GPU Temp - {info_list[1]}°C")
        self.cpu_load.setText(f"CPU Load - {info_list[2]}%")
        self.cpu_temp.setText(f"CPU Temp - {info_list[3]}°C")
        self.mem_load.setText(f"Mem usage - {info_list[4]}%")

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
