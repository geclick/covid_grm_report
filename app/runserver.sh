#!/bin/bash

echo "Migrating database"
python manage.py makemigrations --merge --noinput --settings=MERCES.settings.docker
python manage.py makemigrations --noinput --settings=MERCES.settings.docker
python manage.py migrate --noinput --settings=MERCES.settings.docker

echo "Initializing default super admin user, user: admin pass: admin"
python manage.py initadmin --noinput --settings=MERCES.settings.docker --user "admin" --password "admin" --email 'admin@admin.cu'

echo "Collecting static files"
python manage.py collectstatic --noinput
chmod -R 0755 /app/static

echo "Running server"
#python manage.py runserver 0.0.0.0:8443 --settings=MERCES.settings.docker
gunicorn MERCES.wsgi -c /etc/gunicorn.py
