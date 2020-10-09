from .home import HomeWidget
from .spotify.spotify import SpotifyWidget
from .vlc.vlc import VLCWidget
from .smhi.smhi import SmhiWidget
from .launcher.launcher import LauncherWidget
from .explorer.explorer import ExplorerWidget

WIDGETS = (
    SpotifyWidget,
    VLCWidget,
    SmhiWidget,
    LauncherWidget,
    ExplorerWidget
)
