FROM python:3.6

COPY . /app

WORKDIR /app
EXPOSE 5000

RUN pip3 install -r requirements.txt