import json
import requests

apikey = "ed335c969c23f967ed0ceee2604bafe2"
cityname = 'Moscow'
url = 'https://api.openweathermap.org/data/2.5/weather?q=' + cityname + '&appid=' + apikey

data = requests.get(url)

j_data = data.json()

with open('weather.json', 'w') as j_file:
    j_file.write(json.dumps(j_data))

pass

