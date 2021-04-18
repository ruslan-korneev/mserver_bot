#!/bin/bash

VENV=./rvenv
DEPLOY_FLAG=/opt/telebot/deploy_state.flag
DJANGO_USERNAME=username
DJANGO_PASSWORD=password

touch $DEPLOY_FLAG

if [ ! -d $VENV ]; then
    `which python3` -m venv $VENV
    $VENV/bin/pip install -U pip
fi


$VENV/bin/pip install -r requirements.txt

$VENV/bin/python admin/manage.py makemigrations
$VENV/bin/python admin/manage.py migrate

$VENV/bin/python admin/manage.py collectstatic --no-input

# {$DJANGO_SUPERUSER_USERNAME}{$DJANGO_SUPERUSER_PASSWORD}
if [ -n $DJANGO_USERNAME ] && [ -n $DJANGO_PASSWORD ] ; then
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('username', 'admin@example.com', 'password')" | $VENV/bin/python admin/manage.py shell
    # $VENV/bin/python admin/manage.py closepoll $DJANGO_USERNAME $DJANGO_PASSWORD
fi

$VENV/bin/python admin/manage.py runserver 0.0.0.0:8000

rm -f $DEPLOY_FLAG

echo "Run Django"

# $VENV/bin/uwsgi --yaml ./src/uwsgi.yml
