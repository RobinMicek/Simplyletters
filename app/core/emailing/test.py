from create_email import Email_Template

template_number = 2
color_main = "#6D3692"
color_accent = "#8756A8"
color_text = "#000000"
logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Microsoft_logo_%282012%29.svg/1024px-Microsoft_logo_%282012%29.svg.png"
image_cover = ""
footer = "made with ♥ by Robin Míček"
title = "Můj první newsletter"  
perex_header = "Ahoj |?|name|?|,"
perex = "Tohle je ten úplně první testovací newsletter, který jsme vytvořil! Nyní by se měl snad i posílat."
paragraphs = [{
        "image": "https://helpx.adobe.com/content/dam/help/en/photoshop/using/convert-color-image-black-white/jcr_content/main-pars/before_and_after/image-before/Landscape-Color.jpg",
        "header": "Funguje to?",
        "text": "Tohle by snad již mohlo fungovat! Uvidíme no..."
    },
    {
        "image": None,
        "header": "Second",
        "text": "Ipsum Lorem"
    }]
name = "Robin"
slug = "testovaci-newsletterik-BOOM"
user_group = 2

email = Email_Template(template_number, color_main, color_accent, color_text, logo, image_cover, footer, title, perex, perex_header, paragraphs, name, slug, user_group)

email.create_newsletter("testing")
email.send_email(2)