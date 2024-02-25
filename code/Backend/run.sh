echo "Staritng the app"
echo "-----------------------------"

# Activate virtual env

. .venv/bin/activate
export ENV=developement
python3 main.py

deactivate