# Flight Management App

## Install and Run
```console
# install requirements
pip install -r requirements.txt

# migrate models
python ./manage.py makemigrations
python ./manage.py migrate

# load models initial data
python ./manage.py loaddata fixtures/*

# load test data
python ./manage.py loaddata test_data/* 

# run server
python ./manage.py runserver
```
