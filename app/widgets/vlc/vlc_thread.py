from PyQt5.QtCore import pyqtSignal, QThread

from telnetlib import Telnet
from socket import error as socketerror
from configparser import ConfigParser
from time import sleep


class VLCThread(QThread):

    vlc_command = pyqtSignal(int)
    vlc_time = pyqtSignal(list)
    vlc_title = pyqtSignal(str)
    vlc_volume = pyqtSignal(int)
    is_running = pyqtSignal(bool)

    host = "127.0.0.1"
    port = 4212

    def __init__(self, current_path: str) -> None:
        super().__init__()
        self.current_path = current_path

    def run(self) -> None:
        self.vlc_running = False
        self.thread_running = True

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

        while self.thread_running:
            print(self.thread_running)
            print(self.format_seconds(self.get_time()))
            sleep(1)

        self.vlc_title.emit("VLC IS NOT RUNNING")

    def kill_thread(self):
        self.thread_running = False

    def format_seconds(self, seconds: int) -> str:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        return f"{h:02d}:{m:02d}:{s:02d}"

    def set_password(self, password: str) -> None:
        self.tn.read_until(b"Password: ")
        self.run_command(password)

    def run_command(self, command: str) -> list:
        try:
            self.tn.write(command.encode("utf-8") + b"\n")
            output = self.tn.read_until(b"> ").decode("utf-8")
            return output.split("\r\n")[:-1]
        except ConnectionAbortedError:
            self.kill_thread()
            self.vlc_running = False

    def get_length(self) -> int:
        return int(self.run_command("get_length")[0])

    def get_time(self) -> int:
        output = self.run_command("get_time")
        if output:
            if output[0]:
                return int(output[0])
            else:
                return 0
        else:
            return 0

    def toggleplay(self) -> None:
        self.run_command("pause")

    def volume(self) -> int:
        return int(self.run_command("volume")[0])

    def volume_up(self) -> None:
        self.run_command("volup 1")

    def volume_down(self) -> None:
        self.run_command("voldown 1")

    def small_jump_forwards(self) -> None:
        if self.get_time() + 5 < self.get_length():
            self.run_command(f"seek {self.get_time() + 5}")

    def small_jump_backwars(self) -> None:
        if self.get_time() - 5 > 0:
            self.run_command(f"seek {self.get_time() - 5}")

    def big_jump_forwards(self) -> None:
        if self.get_time() + 30 < self.get_length():
            self.run_command(f"seek {self.get_time() + 30}")

    def big_jump_backwars(self) -> None:
        if self.get_time() - 30 > 0:
            self.run_command(f"seek {self.get_time() - 30}")

    def next(self) -> None:
        self.run_command("next")

    def prev(self) -> None:
        self.run_command("prev")