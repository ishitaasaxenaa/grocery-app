# Steps to Run this project

## Applications to be installed
- Redis
- gtk runtime 3 for weasyprint

## *********** Backend  **************
#open wsl/ubuntu Terminal

create venv and install dependencies


### run flask app
run `sh run.sh`

### Start redis server and celery
run `sh workers.sh`

### Start celery beat
#run `sh beat.sh`


## ************ Frontend  ***************
### Install dependencies
run `npm install`

### Start the server
run `npm run serve`

## DEMO VIDEO 
https://drive.google.com/file/d/14Ch6d6QY2wHGkrSjmafDTz98BF83s9jx/view
