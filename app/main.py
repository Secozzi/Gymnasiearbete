from PyQt5.QtCore import QAbstractEventDispatcher
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

from pyqtkeybind import keybinder
from key_binder import WinEventFilter


class InfoPad(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.show()

    def init_ui(self):
        loadUi('app.ui', self)

    def grid_1(self):
        print("Activated Num 7")

    def grid_2(self):
        print("Activated Num 8")

    def grid_3(self):
        print("Activated Num 9")

    def grid_4(self):
        print("Activated Num 4")

    def grid_5(self):
        print("Activated Num 5")

    def grid_6(self):
        print("Activated Num 6")

    def grid_7(self):
        print("Activated Num 1")

    def grid_8(self):
        print("Activated Num 2")

    def grid_9(self):
        print("Activated Num 3")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    info_app = InfoPad()

    keybinder.init()
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F13", info_app.grid_1)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F14", info_app.grid_2)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F15", info_app.grid_3)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F16", info_app.grid_4)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F17", info_app.grid_5)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F18", info_app.grid_6)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F19", info_app.grid_7)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F20", info_app.grid_8)
    keybinder.register_hotkey(info_app.winId(), "Ctrl+F21", info_app.grid_9)

    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    sys.exit(app.exec_())
