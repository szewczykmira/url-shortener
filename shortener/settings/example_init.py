# -*- coding: utf-8 -*-
from .settings import *
# SECURITY WARNING: keep the secret key used in production secret!
# create secret key and put it as SECRET_KEY instead of this empty string
# You can use http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
# Please fill in name, user and password for database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'user': '',
        'password': '',
        'host': '127.0.0.1',
        'port': '5432',
    }
}
