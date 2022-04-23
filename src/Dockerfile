FROM ubuntu:latest

ADD . /opt/edubot
WORKDIR /opt/edubot

RUN apt-get update
RUN apt-get install -y \
    python3 \
    python3-pip

ARG API_KEY=None
ENV API_KEY="${API_KEY}"

RUN pip install -r requirements.txt

CMD ["python3", "bot.py"]