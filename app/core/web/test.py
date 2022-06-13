import requests

data = {
    "firstname": "",
    "surname": "Test",
    "email": "micek.robin@gmail.com"
}

h = {
    "token": "simplyletters./SIWWUARFRDWZURRT"
}

r = requests.post("http://127.0.0.1:5000/connected-apps/register", headers=h, data=data)

print(r.text)