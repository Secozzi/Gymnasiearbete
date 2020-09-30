from .home import HomeWidget
from .spotify.spotify import SpotifyWidget
from .vlc.vlc import VLCWidget
from .smhi.smhi import SmhiWidget

WIDGETS = (
    SpotifyWidget,
    VLCWidget,
    SmhiWidget
)
