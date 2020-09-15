import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope, cache_path=".cache-secozzi"))

# Shows playing devices
res = sp.current_user_playing_track()
print(res)