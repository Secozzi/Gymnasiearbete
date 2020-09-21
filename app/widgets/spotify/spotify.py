import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

scope = "user-read-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

# Shows playing devices
while True:
    res = sp.current_playback()
    ms = round(res["progress_ms"] / 1000)
    m = ms // 60
    s = ms % 60
    print(f"{m}:{s}")
    sleep(0.1)