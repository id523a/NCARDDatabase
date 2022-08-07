# syntax=docker/dockerfile:1
# Modified by Edward Giles from https://docs.docker.com/samples/django/
FROM python:3.9-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY pip-requirements.txt /code/
RUN apt-get update
RUN apt-get install -y apache2 apache2-utils ssl-cert libapache2-mod-wsgi-py3
RUN pip install -r pip-requirements.txt
COPY . /code/
COPY sites-available /etc/apache2/sites-available/
RUN a2dissite 000-default
RUN a2ensite ncard-database
ENTRYPOINT ["apachectl", "-D", "FOREGROUND"]