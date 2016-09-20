# -*- coding: utf-8 -*-
from django.conf import settings

import string
import random

MAX = settings.SHORT_URL_MAX_LEN


def get_random_string():
    choices = string.ascii_letters + string.digits + "="
    return ''.join(random.choice(choices) for _ in xrange(MAX)).replace("=", "")