# Simplyletters

![GitHub](https://img.shields.io/github/license/robinmicek/Simplyletters)
![GitHub last commit](https://img.shields.io/github/last-commit/robinmicek/simplyletters)

![GitHub Release Date](https://img.shields.io/github/release-date/robinmicek/simplyletters)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/robinmicek/simplyletters)

![Lines of code](https://img.shields.io/tokei/lines/github/robinmicek/simplyletters)

Open Source Web based Tool for Creating and Sending Newsletters.

Simplyletters is aiming to be a Central Hub for managing newletters from all of your apps.


## ⚡ Build with ⚡
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)

**External Sources**

* Trumbowyg Rich Text Editor
* Google Fonts & Icons
* Konstantin Savchenko Email Template



## 🔌 How to Deploy 🔌
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

The provided docker image runs on the latest version of _Ubuntu_, feel free to 
change it to e.g. _Alpine_ for smaller and more efficient image/container. 

First build the Docker Image (will be published on Docker Hub in the future)
```bash
$ docker build -t robinmicek/simplyletters .
```
and then run the container
```bash
$ docker run \
--name "<Container Name>" \
\
-p "<Port>":8000 \
\
-e SL_DATABASE_HOST="<Database Host>" \
-e SL_DATABASE_NAME="<Database Name>" \
-e SL_DATABASE_PASSWORD="<Database Password>" \
-e SL_DATABASE_USER="<Database Username>" \
-e SL_SECRET-KEY="<Flask Secret Key for session variables>" \
\
robinmicek/simplyletters
```

![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)

    Heroku ready - Deploy to Heroku with no further configuration necessary

or

![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)

    Run it as a WSGI app using web server like Gunicorn

First install required python packages
```bash
$ pip install -r requirements.txt
``` 
and then run the server

```bash
$ cd /app/core/web
$ gunicorn --bind 0.0.0.0.:"<port>" app:app
```



## 🔐 Enviroment Variables 🔐
Simplyletters runs on **MySQL Database**. Please note that the database needs to be clean **with no data or tables inside**. Otherwise you won't be able to proceed to the *First Time Setup*.

**SL_DATABASE_HOST** - Database host url

**SL_DATABASE_NAME** - Name of the database

**SL_DATABASE_USER** - Database username

**SL_DATABASE_PASSWORD** - Database password

**SL_SECRET-KEY** - Flask secret key for session variables



## 💻 How to Work with Simplyletters 💻

**Groups** - In Simplyletters you cannot send newsletter to only a one certain user *(you can through the API)*, but rather to a group of users. The group is specified when creating API key for signing users up.

**Settings** - Here you can change your email configuration *(you will be prompted to input your email info in the First Time Setup)* and your logo and footer that will be used in newsletters.

**Admin** - Create and delete admin accounts.

**Connected Apps** - Connected app is an app, from which users can sign up for your newsletters.
* First generate an API key for your app. Choose a group to which the users will be assigned.
* Then you send a post request with the user information (it can be like a *sign up for our newsletter* prompt on a website):

```
POST /connected-apps/register
Host: <specify host url>
Token: "simplyletters./<specify token>"
Content-Type: application/json

{
    "firstname": "<specify firstname>",
    "surname": "<specify surname>",
    "email": "<specify email>"
}
```

There is a script written in Python for testing user's signup for newsletter. You can find it at */app/tests/connect_test.py*

**Newletters**
* To create new newsletter go to the newsletters tab and click on the plus icon, fill out the details and click on create.

![New Newsletter](/img/newsletter-new.png)

* You will be redirected back to the page with all newsletters, click on the newly created newsletter and add paragraphs. 

![Newsletter Paragraphs](/img/newsletter-paragraphs.png)

* Using the buttons on top of the newsletter page you can see how the rendered newsletter looks, send the newsletter to the target group or delete it.

**Notes**

* Adding the cover image is optional.

* In the current version of Simplyletters you cannot use double quotes in any text input due to interference with SQL. It should be fixed in future versions.

* You can use **|?|NAME|?|** variable in any of the newsletters texts. When the newsletter is send, it will be replaced with the user's firstname. It will be done for every person in the group the newsletter is targeted on.



## 📲 Create & Send newsletter via API 📲

Sending newsletters via API is mainly meant for usage with other apps. Like sending invoices, reset tokens for forgotten passwords, etc. 

When sending email via API, it can be only delivered to one user/email address and it can only contain one paragraph.

Sending email through API does not require an account with targeted email address created (If there is, it won't make any difference. There is no logic that would pair the email with the account in DB, I was probably just too lazy to implement it 😀).

* First you need to create a group called **"API"**.
* Then send a post request with the newsletter configuration and user's email address. 

```
POST /api/create-newsletter
Host: <specify host url>
user: "<specify admin username>"
password: "<specify admin password>"
Content-Type: application/json

{
    "template-number": <specify template number>,
    "color-main": "<specify main color>",
    "color-accent": "<specify accent color>",
    "color-text": "<specify text color>",
    "title": "<specify title>",
    
    "perex-header": "<specify perex header>",
    "perex": "<specify perex>",

    "paragraphs": {
        "image": "<specify image>",
        "header": "<specify header>",
        "text": "<specify text>"
    },
    "slug": "<specify slug>",
    "email": "<specify email>"
}
```


There is a script written in Python for testing this api endpoint. You can find it at */app/tests/api_test.py*



Made with ❤ by Robin Míček
