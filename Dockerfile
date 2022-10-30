# syntax=docker/dockerfile:1
# Modified by Edward Giles from https://docs.docker.com/samples/django/
FROM python:3.9-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY NCARDDatabase /code/NCARDDatabase/
COPY ncard_app /code/ncard_app/
COPY manage.py /code/manage.py
COPY pip-requirements.txt /code/pip-requirements.txt
RUN apt-get update
RUN apt-get install -y apache2 apache2-utils openssl ssl-cert libapache2-mod-wsgi-py3
RUN pip install -r pip-requirements.txt
COPY sites-available /etc/apache2/sites-available/
RUN a2enmod ssl
RUN a2enmod rewrite
RUN a2dissite 000-default
RUN a2ensite ncard-database
RUN python manage.py collectstatic --noinput
ENTRYPOINT ["apachectl", "-D", "FOREGROUND"]