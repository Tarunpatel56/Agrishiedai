import requests

def fetch_weather(lat=28.6, lon=77.2):

    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,PRECTOT,RH2M&community=AG&longitude={lon}&latitude={lat}&format=JSON&start=20250101&end=20250102"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        temp = list(data["properties"]["parameter"]["T2M"].values())[0]
        rain = list(data["properties"]["parameter"]["PRECTOT"].values())[0]
        humidity = list(data["properties"]["parameter"]["RH2M"].values())[0]

    except:
        temp = 30
        rain = 5
        humidity = 60

    return temp, rain, humidity
