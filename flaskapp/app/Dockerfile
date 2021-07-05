FROM python:3.7-slim-buster

LABEL MAINTAINER="Marina Weber <marina.weber@tum.de>"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

ADD . /var/www/
ADD ./wsgi.py /var/www/wsgi.py
ADD . /var/www/app
ADD ./wsgi.py /var/www/app/wsgi.py

RUN pip install --upgrade pip
ADD ./requirements.txt /var/www/requirements.txt
RUN pip install -r requirements.txt

RUN apt-get install git
RUN git clone https://github.com/networkx/networkx-metis.git
RUN python3 nenetworkx-metis/setup.py install

RUN addgroup -gid $GROUP_ID www
RUN adduser www -uid $USER_ID -ingroup www -shell /bin/sh

USER www

EXPOSE 5000


CMD [ "gunicorn", "-w", "1", "--bind", "0.0.0.0:5000", "wsgi"]