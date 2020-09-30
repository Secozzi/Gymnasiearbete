from PyQt5.QtCore import pyqtSignal, QThread
from datetime import datetime, timedelta
import requests
import json


class SmhiThread(QThread):
    """QThread that retrievs and processes information from the weather
    api provided by https://www.smhi.se

    Signals:
    weather_info - dict
        Informatin given from smhi.
        Index as key:
        [time, temperature, precipitation, icon_number] as key
    """

    weather_info = pyqtSignal(dict)

    LONGITUDE = 11.974546
    LATITUDE = 57.690388
    LOAD_FROM_WEBSITE = False

    def run(self) -> None:
        data = self.get_data()
        output = {}

    def get_data(self):
        if self.LOAD_FROM_WEBSITE:
            smhi_link = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/"
            data_link = smhi_link + "geotype/point/lon/" + str(self.LONGITUDE) + "/lat/" + str(self.LATITUDE) + "/"
            data_link += "data.json"

            return json.loads(requests.get(data_link).text)
        else:
            with open(r"C:\Users\folke\OneDrive\Documents\Programmering\Python\Github\Gymnasiearbete\app\widgets\smhi"
                      r"\data.json", "r") as json_file:
                data = json.load(json_file)
            return data
