import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

res = sp.devices()
pprint(res)