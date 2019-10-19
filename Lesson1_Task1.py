import json
import requests

username = "yarstech"
url = 'https://api.github.com/users/' + username + '/repos'

data = requests.get(url)

j_data = data.json()

with open('repos.json', 'w') as j_file:
    j_file.write(json.dumps(j_data))

pass