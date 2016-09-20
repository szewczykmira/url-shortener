# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

import base64

User = settings.AUTH_USER_MODEL


def convert(origin):
    max = settings.SHORT_URL_MAX_LENGTH
    base64_str = base64.urlsafe_b64encode(origin)
    return base64_str[:max] if len(base64_str) > max else base64_str


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

    def set_short_url(self):
        # TODO: test
        all_shortend = ShortURL.objects.all().values_list('short_url',
                                                          flat=True)
        base64_str = convert(self.original_url[::-1])

        while base64_str in all_shortend:
            base64_str = convert(str(self.pk) + base64_str)
        self.short_url = base64_str

    def save(self, *args, **kwargs):
        self.full_clean()
        super(ShortURL, self).save(*args, **kwargs)
