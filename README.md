# Simplyletters

![GitHub](https://img.shields.io/github/license/robinmicek/simplyletters)
![GitHub last commit](https://img.shields.io/github/last-commit/robinmicek/simplyletters)

Open Source Web based Tool for Creating and Sending Newsletters.

Simplyletters is aiming to be a Central Hub for managing newletters from all of your apps.


## ⚡ Build with ⚡
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)



## 🔌 How to Deploy 🔌
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
Simplyletters runs on **MySQL Database**. Please note that the database needs to be clean **with no data or tables inside**. Otherwise you won't be able to proceed to do the *First Time Setup*.

**SL_DATABASE_HOST** - Database host url

**SL_DATABASE_NAME** - Name of the database

**SL_DATABASE_USER** - Database username

**SL_DATABASE_PASSWORD** - Database password

**SL_SECRET-KEY** - Flask secret key for session variables



## 💻 How to Work with Simplyletters 💻

**Groups** - In Simplyletters you cannot send newsletter to only a one certain user *(you can through the API)*, but rather to a certain group of users. The group is specified when creating API key for signing users up.

**Settings** - Here you can change your email configuration *(you will be prompted to input your email info in the First Time Setup)* and your logo and footer that will be used in newsletters.

**Admin** - Create and delete admin accounts.

**Connected Apps** - Connected app is an app, from which users can sign up for your newsletters.
* First generate an API key for your app (like a website when you have the *Sign Up for Newsletter* prompt). Choose a group to which the users will be assigned.
* Then you send a post request with the user information:

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
* To create new newsletter go to the newsletters app and click on the plus icon, fill out the details and click on create.

![New Newsletter](/img/newsletter-new.png)

* You will be redirected back to the page with all newsletter, click on the newly created newsletter and add paragraphs. 

![Newsletter Paragraphs](/img/newsletter-paragraphs.png)

* Using the buttons on top of the newsletter page you can see how the rendered newsletter looks, send the newsletter to the target group or delete it.

**Notes**

* Adding the cover image is optional.

* In the current version of Simplyletters you cannot use double quotes in any text input due to interference with SQL queries. It should be fixed in future versions.

* You can use **|?|NAME|?|** variable in any of the newsletters texts. When the newsletter is send, it will be replaced with the user's firstname. It will be done for every person in the group the newsletter is targeted on.