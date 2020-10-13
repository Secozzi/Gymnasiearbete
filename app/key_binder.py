#
#    My "Gymnasiearbete" for school 2020
#    Copyright (C) 2020 Folke Ishii
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from PyQt5.QtCore import QAbstractNativeEventFilter, QByteArray
from typing import Union, Tuple
from pyqtkeybind import keybinder


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
    def __init__(self, _keybinder: keybinder) -> None:
        """Create keybinder instance and super init"""
        self.keybinder = _keybinder
        super().__init__()

    def nativeEventFilter(self,
                          eventType: Union['QByteArray', bytes, bytearray],
                          message: "sip.voidptr"
                          ) -> Tuple[bool, int]:
        """Handle native event filter from eventType."""
        ret = self.keybinder.handler(eventType, message)
        return ret, 0
