FROM ubuntu:latest

WORKDIR /simplyletters
COPY . .

RUN apt update -y
RUN apt upgrade -y

RUN apt install python3 python3-pip python3-dev -y

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--chdir", "./app/core/web", "app:app"]