from pprint import pprint

import requests
import json
from datetime import datetime, timedelta


LONGITUDE = 11.974546
LATITUDE = 57.690388
LOAD_FROM_WEBSITE = True


def get_data():
    if LOAD_FROM_WEBSITE:
        smhi_link = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/"
        data_link = smhi_link + "geotype/point/lon/" + str(LONGITUDE) + "/lat/" + str(LATITUDE) + "/"
        data_link += "data.json"

        return json.loads(requests.get(data_link).text)
    else:
        with open("data.json", "r") as json_file:
            data = json.load(json_file)
        return data


def get_info(data):
    _parameters = data["parameters"]

    _time = data["validTime"]
    time = datetime.strptime(_time, "%Y-%m-%dT%H:%M:%SZ")
    pprint(str(time + timedelta(hours=2)))

    for param in _parameters:
        if param["name"] == "t":
            temp = str(round(float(param["values"][0])))
        elif param["name"] == "pmean":
            precipitation = str(param["values"][0])
        elif param["name"] == "msl":
            pass
            #pprint(param["values"][0])
        elif param["name"] == "ws":
            wind_speed = float(param["values"][0])
            #pprint(wind_speed)

    #pprint(str(time))
    pprint(temp)
    pprint(precipitation)
    pprint("------------------------")


#get_info(get_data()["timeSeries"][0])
[get_info(get_data()["timeSeries"][i]) for i in range(12)]
