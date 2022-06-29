import requests

data = {
    "template-number": 2,
    "color-main": "#FFFFFF",
    "color-accent": "#F1F1F1",
    "color-text": "#000000",
    "title": "API TEST 1",
    
    "perex-header": "|?|NAME|?|",
    "perex": "This is api test.",

    "paragraphs": {
        "image": "https://helpx.adobe.com/content/dam/help/en/photoshop/using/convert-color-image-black-white/jcr_content/main-pars/before_and_after/image-before/Landscape-Color.jpg",
        "header": "Funguje to?",
        "text": "Tohle by snad již mohlo fungovat! Uvidíme no..."
    },
    "slug": "Api Test 1"
}

h = {
    "user": "RobinMicek",
    "password": "RobinMicek"
}

r = requests.post("http://127.0.0.1:5000/api/create-newsletter", headers=h, data=data)

print(r.text)