#!/bin/sh
DIR=$(dirname $0)
cd $DIR
#. venv/bin/activate
python --version
python poll.py
