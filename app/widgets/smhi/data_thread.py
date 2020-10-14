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
        {"ti": time, "t": temperature, "p": precipitation, "s": icon_number} as value

    Constants:
    LONGITUDE - float
        Longitude of coordinate
    LATITUDE - float
        Latitude of coordinate
    """

    # Signals
    weather_info = pyqtSignal(dict)

    # Constants
    LONGITUDE = 11.974546
    LATITUDE = 57.690388

    def run(self) -> None:
        """Function called when thread is started.

        Retrieves data from API and iterates through it,
        adds desired data to output."""

        data = self.get_data()
        output = {}

        for i in range(24):
            _data = data["timeSeries"][i]
            parameters = _data["parameters"]

            time = datetime.strptime(_data["validTime"], "%Y-%m-%dT%H:%M:%SZ")
            time = time + timedelta(hours=2)
            time = str(datetime.strftime(time, "%H:%M"))

            param_dict = {"ti": time}

            for param in parameters:
                if param["name"] == "t":
                    temp = str(round(float(param["values"][0])))
                    param_dict["t"] = temp
                elif param["name"] == "pmean":
                    precipitation = str(param["values"][0])
                    param_dict["p"] = precipitation
                elif param["name"] == "Wsymb2":
                    symbol = int(param["values"][0])
                    param_dict["s"] = symbol

            output[i] = param_dict

        self.weather_info.emit(output)

    def get_data(self) -> dict:
        """Load data from json file given by the API"""

        smhi_link = (
            "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/"
        )
        data_link = (
            smhi_link
            + "geotype/point/lon/"
            + str(self.LONGITUDE)
            + "/lat/"
            + str(self.LATITUDE)
            + "/"
        )
        data_link += "data.json"

        return json.loads(requests.get(data_link).text)
