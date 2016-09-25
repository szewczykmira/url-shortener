# Url-shortener

## Prerequisites
1. Python version 2.7
2. pip

## Installation quide
1. Install dependencies **pip install -r requirements.txt**
2. Set **secret_key** `export SECRET_KEY="12345"`
3. Copy file `settings/example_init.py` to `settings/__init__.py`
4. Define database creditentials in `settings/__init__.py`
5. Prepare database `python manage.py migrate`
6. Run server `python manage.py runserver`
