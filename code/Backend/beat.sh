#! /usr/bin/bash
echo "Startng celery beat"
echo "-----------------------------"

# Activate virtual env

. .venv/bin/activate
export ENV=developement

celery -A main.celery beat --max-interval 1 -l info

deactivate