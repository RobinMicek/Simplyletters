import requests

data = {
        "newsletter": {
            "content": {
                "template_number":  "1",
                "color_main": "#FFF",
                "color_accent": "FFF", 
                "color_text": "000",
                "logo": "",
                "footer": "", 
                "title": "v.2 API Test Newsletter", 
                "perex": "Lorem Ipsum.", 
                "perex_header": "Lipsum!",
                "paragraphs": [
                    {
                        "image": "",
                        "text": "Test 1",
                        "header": "Test 1!"
                    },
                    {
                        "image": "",
                        "text": "Test 2",
                        "header": "Test 2!"
                    }
                ],
                "slug": "v.2_api_test_newsletter", 
                "user_group": "1"
            },
            "info": {
                "send_group": "true",
                "email": ""
            }
        }
    }

h = {
    "user": "<specify username (with API level access)>",
    "password": "<specify password (with API level access)>"
}

r = requests.post("<specify url>/api/create-newsletter", headers=h, json=data)

print(r.text)