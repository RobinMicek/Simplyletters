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
* [SB Admin 2](https://github.com/StartBootstrap/startbootstrap-sb-admin-2) Dashboard
* Konstantin Savchenko Email Template



## 🔌 How to Deploy 🔌
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

The provided docker image runs on the latest version of _Ubuntu_, feel free to 
rebuild the image (from the Dockerfile) to e.g. _Alpine_ for smaller and more efficient image/container. 

First pull the Docker Image from Docker Hub (https://hub.docker.com/r/robinmicek/simplyletters)
```bash
$ docker pull robinmicek/simplyletters:<specify release version (e.g. "v2.0")>
```
and then create a container
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


![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)

    Run it as a WSGI app using web server like Gunicorn

First install the required python packages
```bash
$ pip install -r requirements.txt
``` 
and then run the server

```bash
$ gunicorn --bind 0.0.0.0.:"<port>" --chdir /app/core/web app:app
```



## 🔐 Enviroment Variables 🔐
Simplyletters runs on **MySQL Database**. Please note that the database needs to be clean **with no data or tables inside**. Otherwise you won't be able to proceed to the *First Time Setup*.

**SL_DB_HOST** - Database host url

**SL_DB_NAME** - Name of the database

**SL_DB_USER** - Database username

**SL_DB_PASSWORD** - Database password

**SL_DB_SSL_CA** - Path to the certificate (if using SSL)

**SL_FLASK_SECRET_KEY** - Flask secret key for session variables



## 💻 How to Work with Simplyletters 💻

**Groups** - In Simplyletters you can send newsletter to only a certain email or to a group of users (e.g. all the people that have signed up for a newsletter on your website). The group is specified when creating API key for signing users up.

**Settings** - Here you can change the logo and footer that will be used in your newsletters.

**Admins** - For managing accounts.

**Connect Apps** - Connected app is an app, from which users can sign up for your newsletters.
* First generate an API key for your app. Choose a group to which the users will be assigned.
* Then you send a post request with the user information (it can be like a *sign up for our newsletter* prompt on a website):

```
POST /connect-app/register
Host: <specify host url>
Token: <specify connect token>
Content-Type: application/json

{
    "firstname": "<specify firstname>",
    "surname": "<specify surname>",
    "email": "<specify email>"
}
```

There is a script written in Python for testing user's signup for newsletter. You can find it at *./app/tests/connect_test.py*

**Newletters**
* To create new newsletter go to the newsletters tab and click on the plus icon, fill out the details and click on create.

![New Newsletter](/img/newsletter-new.png)

* Then you can add and manage paragraphs in your newsletter. 

![Newsletter Paragraphs](/img/newsletter-paragraphs.png)

* Using the buttons on top of the newsletter page you can see how the rendered newsletter looks, send the newsletter to the target group or email address, or delete it.

**Notes**

* Adding the cover image is optional.

* You can use **|?|NAME|?|** variable in any of the newsletters texts. When the newsletter is sent, it will be replaced with the user's firstname. It will be done for every person in the group the newsletter is targeted on.



## 📲 Create & Send newsletter via API 📲

Sending newsletters via API is mainly meant for usage with other apps. Like sending invoices, reset tokens for forgotten passwords, etc. 

Email sent through the API can be either delivered to a single email, or to a target group.

If you want to only send newsletter to a single email, the user with that email is not required to be signed on Simplyletters.

* To create and send a newsletter you will first need to create an admin with API level access in the **Admins** tab. 
* Then you need post a request with the newsletter configuration. 

```
POST /api/create-newsletter
Host: <specify host url>
user: <specify username (with API level access)>,
password: <specify password (with API level access)>
Content-Type: application/json

{
    "newsletter": {
        "content": {
            "template_number":  "<specify template number>",
            "color_main": "<specify main color>",
            "color_accent": "<specify accent color>", 
            "color_text": "<specify text color>",
            "logo": "<leave blank - will the pulled from the general config>",
            "footer": "<leave blank - will the pulled from the general config>", 
            "title": "<specify title>", 
            "perex": "<specify perex>", 
            "perex_header": "<specify heading>",
            "paragraphs": [
                {
                    "image": "<specify image>",
                    "text": "<specify text>",
                    "header": "<specify heading>"
                }
            ],
            "slug": "<specify slug>", 
            "user_group": "<specify target group>"
        },
        "info": {
            "send_group": "<true / false>",
            "email": "<specify email>"
        }
    }
}
```

*  If you want to send the newsletter to a target group, then fill the _user_group_ value with the target group id, set the _send_group_ to "true" and leave the _email_ blank.

*  If you want to send the newsletter to a single email address, then fill the _email_ value with the desired email address, set _send_group_ to "false" and fill the _user_group_ with a placeholder value - you need to assign it to some group (I would recommend creating a new group called e.g. _API_ and assigning these newsletter to that).


There is a script written in Python for testing this api endpoint. You can find it at *./app/tests/api_test.py*



## 📣 New features in v2 📣

* New dashboard - [SB Admin 2](https://github.com/StartBootstrap/startbootstrap-sb-admin-2)
* Limit access by assigning _access levels_ to admin accounts
* You can now select if you want to send the newsletter to a target group or an email (both in UI and through API)
* Newsletters created through the API can now have multiple paragraphs


Made with ❤ by Robin Míček
