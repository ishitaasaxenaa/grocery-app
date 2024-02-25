echo "Startng celery"
echo "-----------------------------"

# Activate virtual env

. .venv/bin/activate
export ENV=developement
echo "Starting the redis server"
sudo service redis-server start

echo "Starting the celery worker"
celery -A main.celery worker -l info


deactivate