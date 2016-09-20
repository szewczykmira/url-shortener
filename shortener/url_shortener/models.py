# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

import base64

User = settings.AUTH_USER_MODEL


@python_2_unicode_compatible
class ShortURL(models.Model):
    original_url = models.URLField(verbose_name=_("Original url"),
                                   unique=True, help_text='http://example.com')
    short_url = models.TextField(verbose_name=_("Short url"), unique=True)
    user = models.ForeignKey(User, verbose_name=_("Submitter"))

    class Meta:
        ordering = ['original_url']

    def __str__(self):
        return self.original_url

    def save(self, *args, **kwargs):
        self.full_clean()
        super(ShortURL, self).save(*args, **kwargs)
