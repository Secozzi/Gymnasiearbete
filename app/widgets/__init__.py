from .home import HomeWidget
from .spotify.spotify import SpotifyWidget
from .vlc.vlc import VLCWidget
from .smhi.smhi import SmhiWidget
from .launcher.launcher import LauncherWidget

WIDGETS = (
    SpotifyWidget,
    VLCWidget,
    SmhiWidget,
    LauncherWidget
)
