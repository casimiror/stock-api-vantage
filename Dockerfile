FROM python:3.6.9-buster

RUN apt-get update

RUN mkdir -p /config
ADD requirements.txt /config/
RUN pip install -r /config/requirements.txt
RUN apt-get update && apt-get install -y gettext libgettextpo-dev
ADD . /usr/src/app
WORKDIR /usr/src/app

COPY init.sh /usr/local/bin/init.sh
RUN chmod u+x /usr/local/bin/init.sh
