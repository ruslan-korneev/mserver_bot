#!/bin/bash

VENV=./rvenv
DEPLOY_FLAG=/opt/telebot/deploy_state.flag

touch $DEPLOY_FLAG

if [ ! -d $VENV ]; then
    `which python3` -m venv $VENV
    $VENV/bin/pip install -U pip
fi

$VENV/bin/python -m pip install --upgrade pip
$VENV/bin/pip install -r requirements.txt

# $VENV/bin/python src/bot_admin/manage.py migrate --fake sessions zero
# $VENV/bin/python src/bot_admin/manage.py migrate --fake
# $VENV/bin/python src/bot_admin/manage.py migrate --fake-initial
# $VENV/bin/python src/bot_admin/manage.py makemigrations

$VENV/bin/python src/bot_admin/manage.py migrate
$VENV/bin/python src/bot_admin/manage.py collectstatic --no-input

# $VENV/bin/python src/bot_admin/manage.py createmysuperuser
# echo "from django.contrib.auth.models import User; 
# 	User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${MAIL}', '${DJANGO_SUPERUSER_PASSWORD}')" | 
# 	$VENV/bin/python src/bot_admin/manage.py shell

$VENV/bin/python src/bot_admin/manage.py runserver 0.0.0.0:8000

rm -f $DEPLOY_FLAG

echo "Run Django"

# $VENV/bin/uwsgi --yaml ./src/uwsgi.yml



