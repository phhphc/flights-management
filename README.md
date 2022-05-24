# Flights Management App

## About this project
This project allows businesses to manage flights and customer to book online tickets via web platform.

## About our team
| Student ID | Fullname                                        |
| ---------- | ----------------------------------------------- |
| 19120454   | [Bùi Quang Bảo](https://github.com/buiquangbao) |
| 19120331   | [Phạm Lưu Mỹ Phúc](https://github.com/plphuc)   |
| 19120301   | [Võ Thành Nam](https://github.com/thanhnam001)  |
| 19120315   | [Lương Ánh Nguyệt](https://github.com/nnguyet)  |
| 19120120   | [Phạm Hữu Phước](https://github.com/phhphc)     |

## References
- https://docs.djangoproject.com/en/4.0/
- https://www.youtube.com/watch?v=xv_bwpA_aEA&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO

## Execute Environment
- **OS**: Windows, linux
- **SDK**: Python, Django
- **Database**: PostgreSQL, SQLite
- **Dev Tool**: Visual studio code, Firefox DevTools, Chrome DevTools 

## Local Setup
```bash
# create environment variable
cp ./.env.example ./.env
# then manually edit enviroment variable from .env file

# install requirements
pip install -r requirements.txt

# migrate models
python ./manage.py makemigrations
python ./manage.py migrate

# load models initial data
python ./manage.py loaddata fixtures/*

# load test data
python ./manage.py loaddata ./test_data/*

# run server
python ./manage.py runserver
```

About test data:
- admin user: `root:0000`
- user1 : `user1:0000`
- user2 : `user2:0000`
- user3 : `user3:0000`
- user4 : `user4:0000`

## Heroku deploy
```bash
# login to heroku cli
heroku login

# create heroku app
heroku create -a flights-management-hcmus2022

# config App Envioment variable 
heroku config:set DEBUG=False -a flights-management-hcmus2022
heroku config:set SECRET_KEY='eqe@#$@#%$%^fwe2eq2e./,' -a flights-management-hcmus2022

# install heroku postgres addon (free)
heroku addons:create heroku-postgresql:hobby-dev -a flights-management-hcmus2022
## we may need to manually add data to database (use heroku console for faster speed)

# add remote to local repository
heroku git:remote -a flights-management-hcmus2022

# deploy to heroku
git push heroku
```

## Live Demo
- https://flights-management-hcmus2022.herokuapp.com/

## Video demo
- Update later

## Current status
- [x] implement database
- [x] allow login
- [x] list flight list
- [x] view flight detail
- [x] book flight
- [x] implement payment method
- [x] allow customer to view book hostory
- [x] manage user infomation
- [x] alow admin to add flight
- [x] limit minimum flight duration
- [x] limit maximun intermediate airport
- [x] limit minimum/maximun stop time at intermediate airport
- [x] allow employee create/edit/remove flight ticket
- [x] only alow book ticket when there are seat avalible
- [x] allow customer to book ticket
- [x] allow customer to cancel ticket
- [x] allow guest to book ticket
- [x] find ticket, flight by city name
- [x] report revenue monthly/annual
- [x] update airports 
- [x] update ticket classes
- [ ] implement web UI
- [ ] user testing
- [ ] perfoment testing

## Future Work
- [ ] Update later
