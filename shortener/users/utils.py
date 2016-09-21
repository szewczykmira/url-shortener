# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from random import randint

User = get_user_model()


def get_random_user():
    """
    Returns random user, if there is none then returns False
    """
    count = User.objects.all().count()
    if not count:
        raise User.DoesNotExist
    random = randint(0, count - 1)
    return User.objects.all()[random]
