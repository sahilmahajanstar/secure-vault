#!/bin/bash

mkdir -p data 
touch data/db.sqlite3
python manage.py migrate  
python create_superuser.py