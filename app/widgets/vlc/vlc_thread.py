from PyQt5.QtCore import pyqtSignal, QThread

from typing import Union
from telnetlib import Telnet
from socket import error as socketerror
from configparser import ConfigParser
from time import sleep


class VLCThread(QThread):
    """QThread that gets information and sends commands to VLC
    instance.

    Signals:
    vlc_time - list
        List containing current elapsed time and
        movie duraion, in that order. If nothing is
        played, [0, 0] is emitted.
    vlc_title - str
        String contaning the title of the movie
    vlc_volume - int
        Volume of VLC instance
    is_running - bool
        bool corresponing to whether VLC is running
        or not.

    Constans:
    host - str
        IP adress of the host of the vlc instance
    port - int
        Telnet port of the host
    """

    # Signals
    vlc_time = pyqtSignal(list)
    vlc_title = pyqtSignal(str)
    vlc_volume = pyqtSignal(int)
    is_running = pyqtSignal(bool)

    # Constants
    host = "127.0.0.1"
    port = 4212

    def __init__(self, current_path: str) -> None:
        super().__init__()
        self.current_path = current_path

    def run(self) -> None:
        """Function called when thread is started.

        Creates Telnet instance, reads password
        from credentials.cfg and sets password.
        Every 0.5 seconds, emit information about
        current movie played on VLC instance.
        """
        self.vlc_running = False
        self.thread_running = True
        self.tn = None

        try:
            self.tn = Telnet(self.host, self.port)
        except socketerror:
            self.vlc_running = False
        else:
            self.vlc_running = True
            self.vlc_title.emit("VLC IS RUNNING")

        if self.vlc_running:
            try:
                credentials = ConfigParser()
                credentials.read(f"{self.current_path}/credentials.cfg")
                vlc_password = credentials["VLC"]["PASSWORD"]
                self.set_password(vlc_password)
            except Exception as e:
                print(e)
        else:
            self.vlc_title.emit("VLC IS NOT RUNNING")

        if self.tn:
            while self.thread_running:
                current_time = self.format_seconds(self.get_time())
                duration = self.format_seconds(self.get_length())
                volume = self.get_volume()
                title = self.get_title()

                self.vlc_time.emit([current_time, duration])
                self.vlc_volume.emit(volume)
                self.vlc_title.emit(title)
                sleep(0.5)

        # When thread is stopped
        self.vlc_title.emit("VLC IS NOT RUNNING")

    def kill_thread(self) -> None:
        """Sets thread_running flag to false, thus stopping thread"""
        self.thread_running = False

    def format_seconds(self, seconds: int) -> str:
        """Format seconds into HOUR:MINUTES:SECONDS format"""
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        return f"{h:02d}:{m:02d}:{s:02d}"

    def set_password(self, password: str) -> None:
        """Sets password on telnet instance"""
        self.tn.read_until(b"Password: ")
        self.run_command(password)

    def run_command(self, command: str) -> Union[list, None]:
        """Runs command via Telnet on VLC instance and returns output"""
        try:
            self.tn.write(command.encode("utf-8") + b"\n")
            output = self.tn.read_until(b"> ").decode("utf-8")
            return output.split("\r\n")[:-1]
        except ConnectionAbortedError:
            self.kill_thread()
            self.vlc_running = False

    def get_length(self) -> int:
        """Get movie duration on VLC instance"""
        length = self.run_command("get_length")
        if length == [""]:
            return 0
        else:
            return int(length[0])

    def get_time(self) -> int:
        """Get time elapsed on movie on VLC instance"""
        output = self.run_command("get_time")
        if output == [""]:
            return 0
        else:
            return int(output[0])

    def toggleplay(self) -> None:
        """Toggle play/pause on VLC instance"""
        self.run_command("pause")

    def get_volume(self) -> int:
        """Gets volume on VLC instance"""
        volume = self.run_command("volume")
        if volume == [""]:
            return 0
        else:
            return int(volume[0])

    def volume_up(self) -> None:
        """Run command to increase volume by 5%"""
        self.run_command("volup 1")

    def volume_down(self) -> None:
        """Run command to lower volume by 5%"""
        self.run_command("voldown 1")

    def small_jump_forwards(self) -> None:
        """Check if more than 5 seconds left and if so,
        jump forwards 5 seconds."""
        if self.get_time() + 5 < self.get_length():
            self.run_command(f"seek {self.get_time() + 5}")

    def small_jump_backwars(self) -> None:
        """Check if more than 5 seconds has passed and if so,
        jump back 5 seconds."""
        if self.get_time() - 5 > 0:
            self.run_command(f"seek {self.get_time() - 5}")

    def big_jump_forwards(self) -> None:
        """Check if more than 30 seconds left and if so,
        jump forwards 30 seconds."""
        if self.get_time() + 30 < self.get_length():
            self.run_command(f"seek {self.get_time() + 30}")

    def big_jump_backwars(self) -> None:
        """Check if more than 30 seconds has passed and if so,
        jump back 30 seconds."""
        if self.get_time() - 30 > 0:
            self.run_command(f"seek {self.get_time() - 30}")

    def next(self) -> None:
        """Runs command to start previous movie in playlist"""
        self.run_command("next")

    def prev(self) -> None:
        """Runs command to start next movie in playlist"""
        self.run_command("prev")

    def get_title(self) -> str:
        """Gets title of current movie played"""
        title = self.run_command("get_title")
        if title == ['']:
            return ""
        else:
            return title[0]
