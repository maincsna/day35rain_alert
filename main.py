

import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWN_Endpoint = "https://api.openweathermap.org/data/3.0/onecall"

api_key = "9f8ea01b8ba60b05d15334b0c1fcf266"
account_sid = 'AC94b6688c7cdc5e893b5a971c65682e14'
auth_token = '02049b03ca5c3bde2c035a112e8f1f76'

weather_params ={
    # "lat": 37.368832,
    "lat": 39.768402,
    #"lon": -122.036346,
     "lon": -86.158066,
    "appid":api_key,
    "exclude":"current, minutely,daily"
}

response = requests.get(OWN_Endpoint,params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an umbrella",
        from_='+16822973785',
        to='+3107458919',
    )
    print(message.status)


# print(weather_data["hourly"][0]["weather"][0]["id"])

