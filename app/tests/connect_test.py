import requests

url = "<specify url>/connect-app/register"

headers = {
    "Token": "<specify connect token>"
}

data = {
"firstname": "<specify firstname>",
"surname": "<specify surname>",
"email": "<specify email>"
}



resp = requests.post(url, headers=headers, json=data)

print(resp.text)

