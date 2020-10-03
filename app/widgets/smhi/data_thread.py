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

    def run(self) -> None:
        data = self.get_data()
        output = {}

        for i in range(24):
            _data = data["timeSeries"][i]
            parameters = _data["parameters"]

            time = datetime.strptime(_data["validTime"], "%Y-%m-%dT%H:%M:%SZ")
            time = time + timedelta(hours=2)
            time = str(datetime.strftime(time, "%H:%M"))

            param_list = [time]

            for param in parameters:
                if param["name"] == "t":
                    temp = str(round(float(param["values"][0])))
                    param_list.append(temp)
                elif param["name"] == "pmean":
                    precipitation = str(param["values"][0])
                    param_list.append(precipitation)
                elif param["name"] == "Wsymb2":
                    symbol = int(param["values"][0])
                    param_list.append(symbol)

            output[i] = param_list

        self.weather_info.emit(output)

    def get_data(self) -> dict:
        smhi_link = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/"
        data_link = smhi_link + "geotype/point/lon/" + str(self.LONGITUDE) + "/lat/" + str(self.LATITUDE) + "/"
        data_link += "data.json"

        return json.loads(requests.get(data_link).text)
