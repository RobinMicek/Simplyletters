import requests

url = "http://simplyletters.herokuapp.com/connected-apps/register"

headers = {
    "Token": "simplyletters./IFTROGUESWZWORFG"
}

data = {
"firstname": "<specify firstname>",
"surname": "<specify surname>",
"email": "<specify email>"
}



resp = requests.post(url, headers=headers, json=data)

print(resp.text)

