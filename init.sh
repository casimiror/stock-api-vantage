#!/bin/bash
while read var; do export $var; done < /usr/src/app/.env

python /usr/src/app/manage.py makemigrations
python /usr/src/app/manage.py migrate


/usr/local/bin/gunicorn --chdir=/usr/src/app stockemmender.wsgi -b 0.0.0.0:8000 --reload --worker-class=gevent --worker-connections=1000 --workers=8 -t 300
