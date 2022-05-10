# Flight Management App

## Install and Run
```bash
# create environment variable
cp ./.env.example ./.env
## manually edit .env file

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

## About Test Data
### User List
- admin user: `root:0000`
- user1 : `user1:0000`
- user2 : `user2:0000`
- user3 : `user3:0000`
- user4 : `user4:0000`
