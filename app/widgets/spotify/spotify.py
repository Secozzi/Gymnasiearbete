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

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi

from configparser import ConfigParser
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import requests


class SpotifyWidget(QWidget):
    """Spotify application. It displays the cover image,
    the artist name and song name."""

    display_name = "Spotify"

    def __init__(self, main_window: 'InfoPad') -> None:
        super().__init__()
        self.main_window = main_window

        loadUi(f"{self.main_window.current_path}/widgets/spotify/spotify.ui", self)
        self.track_icon.setScaledContents(True)

    @staticmethod
    def get_icon(curr_path: str) -> QPixmap:
        return QPixmap(f"{curr_path}/widgets/spotify/spotify.png")

    def on_enter(self) -> None:
        """Read client_id, client_secret, and redirect_uri from credentials.cfg.
        It will then create a spotipy instance and retrieve cover image, artist
        name, and song name from current playing song.
        """
        self.credentials = ConfigParser()
        self.credentials.read(f"{self.main_window.current_path}/credentials.cfg")

        client_id = self.credentials["SPOTIPY"]["CLIENT_ID"]
        client_secret = self.credentials["SPOTIPY"]["CLIENT_SECRET"]
        redirect_uri = self.credentials["SPOTIPY"]["REDIRECT_URI"]

        scope = "user-read-playback-state"
        self.sp = Spotify(client_credentials_manager=SpotifyOAuth(client_id=client_id,
                                                                  client_secret=client_secret,
                                                                  redirect_uri=redirect_uri,
                                                                  cache_path=f"{self.main_window.current_path}/.cache",
                                                                  scope=scope))

        self.res = self.sp.current_playback()

        if self.res:
            if self.res["item"]["album"]["images"]:
                largest_img = self.res["item"]["album"]["images"][0]["url"]

                self.image = requests.get(largest_img).content
                self.image_pixmap = QPixmap()
                self.image_pixmap.loadFromData(self.image)

                self.track_icon.setPixmap(self.image_pixmap)
            else:
                self.image = None
                self.image_pixmap = QPixmap(f"{self.main_window.current_path}/widgets/spotify/no_image.png")

                self.track_icon.setPixmap(self.image_pixmap)

            song_name = self.res["item"]["name"]
            artist = self.res["item"]["artists"][0]["name"]

            self.track_artist.setText(artist)
            self.track_song.setText(song_name)
        else:
            self.image = None
            self.image_pixmap = QPixmap(f"{self.main_window.current_path}/widgets/spotify/no_image.png")

            self.track_icon.setPixmap(self.image_pixmap)
            self.track_artist.setText("Nothing playing")
            self.track_song.setText("Nothing playing")

    def on_exit(self) -> None:
        """Clear labels and delete variables in order to save memory"""
        self.track_icon.clear()
        self.track_artist.clear()
        self.track_song.clear()

        if self.res:
            del self.image
            del self.image_pixmap
            del self.credentials
            del self.res
            del self.sp

    def grid_1(self) -> None:
        pass  # Num 4

    def grid_2(self) -> None:
        pass  # Num 5

    def grid_3(self) -> None:
        pass  # Num 6

    def grid_4(self) -> None:
        pass  # Num +

    def grid_5(self) -> None:
        pass  # Num 1

    def grid_6(self) -> None:
        pass  # Num 2

    def grid_7(self) -> None:
        pass  # Num 3

    def grid_8(self) -> None:
        pass  # Num Enter

    def grid_9(self) -> None:
        pass  # Num 9

    def grid_sd(self) -> None:
        pass  # Num 7

    def grid_su(self) -> None:
        pass  # Num 8

    def grid_view_o(self) -> None:
        pass  # Num Page Down
