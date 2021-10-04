# Django learning management system
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
## General info
Learning management system web-app was made using djnago 3

In this app user can get permission from admin to post their online lessons, admin can control who can post, edit, delete posts.
Users who want to learn can access courses by enrolling them.

## Technologies
Project is created with:
* asgiref==3.3.4
* Django==3.2.4
* django-materializecss-form==1.1.17
* Pillow==8.2.0
* psycopg2==2.8.6
* pytz==2021.1


## Setup
To run this app on your local machine install dependencies using pip:
```
pip install -r requirements.txt
```
Create superuser:
```
python manage.py createsuperuser
```
Make migrations:
```
python manage.py migrate
```
Run:
```
python manage.py runserver
```
