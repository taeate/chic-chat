FROM python:3.10

WORKDIR /usr/src/app
# 이거 한얼님이 하신거잔항요 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ
COPY . .
RUN pip3 install -r requirements/prod.txt