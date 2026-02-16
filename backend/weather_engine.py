import requests

def fetch_weather():

    url = "https://api.open-meteo.com/v1/forecast?latitude=28.6&longitude=77.2&current_weather=true"

    response = requests.get(url)
    data = response.json()

    weather = data.get("current_weather", {})

    return {
        "temperature": weather.get("temperature"),
        "windspeed": weather.get("windspeed")
    }
