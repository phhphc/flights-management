# Flight Management App

## Install and Run
```sh
# install requirements
pip install -r requirements.txt

# migrate models
python ./manage.py makemigrations
python ./manage.py migrate

# load models initial data
python ./manage.py loaddata fixtures/*

# run server
python ./manage.py runserver
```