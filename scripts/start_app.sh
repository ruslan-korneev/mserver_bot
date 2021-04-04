#!/bin/bash

VENV=../rvenv
DEPLOY_FLAG=../deploy_state.flag

touch $DEPLOY_FLAG

if [ ! -d $VENV ]; then
    which python3 -m venv $VENV
    $VENV/bin/pip install -U pip
    $VENV/bin/pip install --upgrade pip
fi

$VENV/bin/pip install -r ../requirements.txt
$VENV/bin/python ../src/servstatsbot.py