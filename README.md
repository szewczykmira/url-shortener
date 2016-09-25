# Url-shortener

## Prerequisites
1. Python version 2.7
2. pip

## Installation quide
1. Install dependencies **pip install -r requirements.txt**
2. Set **secret_key** `export SECRET_KEY="12345"`
3. Copy file _settings/example_init.py_ to _settings/__init__.py_
4. Prepare database `python manage.py migrate`
5. Run server `python manage.py runserver`
