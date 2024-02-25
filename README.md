Steps to Run this project

Applications to be installed
- Redis
- gtk runtime 3 for weasyprint

*********** Go to Backend Folder **************
#open wsl/ubuntu Terminal

create venv and install dependencies


run `sh run.sh`
# Will run flask app


run `sh workers.sh`
# Starts redis server and celery

#run `sh beat.sh`
# Starts celery beat


************ Go to Frontend folder ***************
run `npm install`
# installs dependencies

run `npm run serve`
#starts the server
