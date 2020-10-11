from .home import HomeWidget
from .spotify.spotify import SpotifyWidget
from .vlc.vlc import VLCWidget
from .smhi.smhi import SmhiWidget
from .launcher.launcher import LauncherWidget
from .explorer.explorer import ExplorerWidget
from .system.system import SystemWidget

WIDGETS = (
    SpotifyWidget,
    VLCWidget,
    SmhiWidget,
    LauncherWidget,
    ExplorerWidget,
    SystemWidget
)
