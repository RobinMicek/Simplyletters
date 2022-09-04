import requests

data = {
    "template-number": 2,
    "color-main": "#FFFFFF",
    "color-accent": "#F1F1F1",
    "color-text": "#000000",
    "title": "API TEST",
    
    "perex-header": "Hi,",
    "perex": "this is an api test.",

    "paragraphs": {
        "image": "https://helpx.adobe.com/content/dam/help/en/photoshop/using/convert-color-image-black-white/jcr_content/main-pars/before_and_after/image-before/Landscape-Color.jpg",
        "header": "Api testing!",
        "text": "This newsletter was made and sent via the Simplyletters API"
    },
    "slug": "Api Test 1",
    "email": "<specify email>"
}

h = {
    "user": "<username>",
    "password": "<password>"
}

r = requests.post("<specify host>/api/create-newsletter", headers=h, json=data)

print(r.text)