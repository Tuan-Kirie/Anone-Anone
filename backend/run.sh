#!/bin/bash
# pipenv shell
case $1 in
  dev)
    python manage.py runserver --settings=anone.settings.devw
    ;;
  prod)
    python manage.py collectstatic --noinput
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver --settings=anone.settings.prod
     ;;
esac