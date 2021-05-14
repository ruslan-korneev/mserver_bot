#!/bin/bash

VENV=./rvenv
DEPLOY_FLAG=/opt/telebot/deploy_state.flag

touch $DEPLOY_FLAG

if [ ! -d $VENV ]; then
    `which python3` -m venv $VENV
    $VENV/bin/pip install -U pip
fi

$VENV/bin/pip install -r requirements.txt

$VENV/bin/python src/bot/bot.py

rm -f $DEPLOY_FLAG

echo "Run Bot"