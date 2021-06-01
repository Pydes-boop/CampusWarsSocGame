FROM python:3.6.8-alpine3.9

LABEL MAINTAINER="Marina Weber <marina.weber@tum.de>"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

ADD ./requirements.txt /var/www/requirements.txt
RUN pip install -r requirements.txt
RUN pip install flask

RUN pip install flask-restful
RUN pip install flask-pymongo
RUN pip install flask-mongoengine
ADD . /var/www/
ADD ./wsgi.py /var/www/wsgi.py
ADD . /var/www/app
ADD ./wsgi.py /var/www/app/wsgi.py
RUN pip install gunicorn

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www

EXPOSE 5000


CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi"]