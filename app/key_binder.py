from PyQt5.QtCore import QAbstractNativeEventFilter


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0

"""
Numpad7 - Grid 1        - CTRL + F13
Numpad8 - Grid 2        - CTRL + F14
Numpad9 - Grid 3        - CTRL + F15
Numpad4 - Grid 4        - CTRL + F16
Numpad5 - Grid 5        - CTRL + F17
Numpad6 - Grid 6        - CTRL + F18
Numpad1 - Grid 7        - CTRL + F19
Numpad2 - Grid 8        - CTRL + F20
Numpad3 - Grid 9        - CTRL + F21
Numpad0 - Grid 10       - CTRL + F22
Numpad, - Grid Home     - Alt + F13
NumpadE - Scroll Down   - Alt + F14
Numpad+ - Scroll Up     - Alt + F15
Numpad- - Vol Up        - Alt + F16
Numpad* - Vol Down      - Alt + F17
Numpad/ - Mute Mic      - Alt + F18
"""
