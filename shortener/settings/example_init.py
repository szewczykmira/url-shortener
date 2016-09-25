# -*- coding: utf-8 -*-
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
# Please fill in name, user and password for database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shortener',
        'user': '',
        'password': '',
        'host': '127.0.0.1',
        'port': '5432',
    }
}
