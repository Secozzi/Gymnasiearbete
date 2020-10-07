# PyQt5
from PyQt5.QtCore import pyqtSignal, QThread

# Audio
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Spotipy
from configparser import ConfigParser
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Other
from os import path
from time import sleep
from datetime import datetime
from psutil import pid_exists, process_iter


CURR_PATH = path.dirname(path.realpath(__file__))

# Get audio device
DEVICES = AudioUtilities.GetSpeakers()
INTERFACE = DEVICES.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
VOLUME = cast(INTERFACE, POINTER(IAudioEndpointVolume))

# Get spotify credentils from credentials.cfg
credentials = ConfigParser()
credentials.read(f"{CURR_PATH}/credentials.cfg")

client_id = credentials["SPOTIPY"]["CLIENT_ID"]
client_secret = credentials["SPOTIPY"]["CLIENT_SECRET"]
redirect_uri = credentials["SPOTIPY"]["REDIRECT_URI"]

# Create Spotipy instance
scope = "user-read-playback-state"
sp = Spotify(client_credentials_manager=SpotifyOAuth(client_id=client_id,
                                                     client_secret=client_secret,
                                                     redirect_uri=redirect_uri,
                                                     cache_path=f"{CURR_PATH}/.cache",
                                                     scope=scope))


class InfoThread(QThread):
    """QThread that gets information and sends it to the main application

    Signals:
    time_s - str
        Current time
    date_s - str
        Current date
    music - str
        Song name, progress, and duration from a Spotify instance
    desktop_volume - int
        System volume in percentage (1-100)

    Constans:
    REFRESH RATE - float
        How long the thread will sleep between each time it gets,
        process, and sends information to main thread.
    MUSIC_LENGTH - int
        How many characters the label showing the music info contains
    SPOT_PID - int
        Current PID of Spotify instance
    """

    # pyqtSignals
    time_s = pyqtSignal(str)
    date_s = pyqtSignal(str)
    music = pyqtSignal(str)
    desktop_volume = pyqtSignal(int)

    # Constants
    REFRESH_RATE = 0.2
    MUSIC_LENGTH = 22
    SPOT_PID = -1

    def run(self) -> None:
        """Function called when thread is started

        Gets PID from spotify, current volume, and information
        about current spotify playback.
        Every "REFRESH_RATE", it gets emitted to main window.
        """

        for p in process_iter():
            if p.name() == "Spotify.exe":
                self.SPOT_PID = p.pid

        while True:
            _master_volume = VOLUME.GetMasterVolumeLevelScalar() * 100
            time_now = datetime.now()

            spotify_info = self.get_spotify_information()

            self.time_s.emit(time_now.strftime("%H:%M:%S"))
            self.date_s.emit(time_now.strftime("V.%V - %a %d %b %Y"))
            self.desktop_volume.emit(round(_master_volume))
            self.music.emit(spotify_info)

            sleep(self.REFRESH_RATE)

    def get_spotify_information(self) -> str:
        """Get song name, duration, and progress from a Spotify instance.

        If Spotify is not running or no song is playing,
        "Nothing playing currently" gets returned.
        """
        if pid_exists(self.SPOT_PID):
            try:
                res = sp.current_playback()
            except Exception:
                res = None
        else:
            res = None

        if res:
            current = self.get_length(res["progress_ms"])
            duration = self.get_length(res["item"]["duration_ms"])

            song_name = res["item"]["name"]

            return f"{current}/{duration} {song_name}"[:self.MUSIC_LENGTH]
        else:
            return "Nothing playing currently"[:self.MUSIC_LENGTH]

    def refresh_spotify(self) -> None:
        """Refresh PID from a Spotify instance"""
        for p in process_iter():
            if p.name() == "Spotify.exe":
                self.SPOT_PID = p.pid

    @staticmethod
    def get_length(ms: int) -> str:
        """Converts milliseconds into MINUTE:SECONDS format"""
        s = round(ms / 1000)
        return f"{(s // 60):02d}:{(s % 60):02d}"
