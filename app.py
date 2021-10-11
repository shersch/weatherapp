from flask import Flask, request
from dotenv import load_dotenv, find_dotenv
import requests
import geocoder
import os
from prettytable import PrettyTable

load_dotenv(find_dotenv())

def owm_req(location, units):
    w_url = "https://api.openweathermap.org/data/2.5/weather?"
    w_params = {"q": location, "units": units, "appid": os.getenv("OWM_KEY")}
    return requests.get(w_url, params=w_params)

def aqi_req(aq_token, lat, lon):
    aq_url = f"https://api.waqi.info/feed/geo:{str(lat)};{str(lon)}/?token={aq_token}"
    return requests.get(aq_url)


app = Flask(__name__)
@app.route("/")
def weather():
    location = request.args.get("location")
    units = request.args.get("units")

    if location is None:
        ip_addr = request.headers.getlist("X-Real-Ip")
        if ip_addr[0] == "192.168.1.1":
            location = geocoder.ip('me').address
        else:
            location = geocoder.ip(ip_addr[0]).address
    if units is None:
        units = "imperial"

    owm = owm_req(location, units)
    lat = owm.json()['coord']['lat']
    lon = owm.json()['coord']['lon']

    aq_req = aqi_req(os.getenv("WAQI_KEY"), lat, lon)

    loc_name = str(owm.json()['name'])
    current = str(owm.json()['main']['temp'])
    high = str(owm.json()['main']['temp_max'])
    low = str(owm.json()['main']['temp_min'])
    humidity = str(owm.json()['main']['humidity']) + "%"
    conditions = owm.json()['weather'][0]['description']
    aqi = aq_req.json()['data']['aqi']


    w_table = PrettyTable()
    w_table.field_names =["Location", loc_name]
    w_table.add_rows(
        [
            ["Current", current],
            ["High", high],
            ["Low", low],
            ["Humidity", humidity],
            ["Conditions", conditions],
            ["AQI", str(aqi)]
        ]
    )
    if "curl" in request.headers.get('User-Agent'):
        return w_table.get_string()
    else:
        return w_table.get_html_string()
