FROM python:3.10

WORKDIR /usr/src/app

COPY . .
RUN pip3 install -r requirements/prod.txt