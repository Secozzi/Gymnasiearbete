from PyQt5.QtCore import QAbstractNativeEventFilter


class WinEventFilter(QAbstractNativeEventFilter):
    """Keybinds:
    /--------------- Page specific ---------------\
    | Numpad7 - Scroll Down   - CTRL + F13        |
    | Numpad8 - Scroll Up     - CTRL + F14        |
    | Numpad9 - Extra key     - CTRL + F15        |
    |                                             |
    | Numpad4 - Grid 1        - CTRL + F16        |
    | Numpad5 - Grid 2        - CTRL + F17        |
    | Numpad6 - Grid 3        - CTRL + F18        |
    | Numpad+ - Grid 4        - CTRL + F19        |
    | Numpad1 - Grid 5        - CTRL + F20        |
    | Numpad2 - Grid 6        - CTRL + F21        |
    | Numpad3 - Grid 7        - CTRL + F22        |
    | NumpadE - Grid 8        - CTRL + F23        |
    |------------------- Global ------------------|
    | Numpad, - Grid Home     - CTRL + Alt + F13  |
    | Numpad- - Mute Mic      - CTRL + Alt + F14  |
    | Numpad* - Opacity Up    - CTRL + Alt + F15  |
    | Numpad/ - Opacity Down  - CTRL + Alt + F16  |
    | NumpadR - View Overlay  - CTRL + Alt + F17  |
    | Numpad0 - Modifier      - Modifier          |
    \---------------------------------------------/
    """
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0
