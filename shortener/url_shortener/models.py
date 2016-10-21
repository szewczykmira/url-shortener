# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from .utils import get_random_string

import base64

User = settings.AUTH_USER_MODEL


@python_2_unicode_compatible
class ShortURL(models.Model):
    original_url = models.URLField(verbose_name=_("Original url"),
                                   unique=True,
                                   help_text=_('Input should look like this:'
                                               ' http://example.com'))
    short_url = models.TextField(verbose_name=_("Short url"), unique=True)
    user = models.ForeignKey(User, verbose_name=_("Submitter"))

    class Meta:
        ordering = ['original_url']

    def __str__(self):
        return self.original_url

    def set_short_url(self):
        short_str = base64.urlsafe_b64encode(self.original_url)
        if ShortURL.objects.exclude(pk=self.pk).filter(
                short_url=short_str).exists() \
                or len(short_str) > settings.SHORT_URL_MAX_LEN:
            short_str = get_random_string()
            while ShortURL.objects.exclude(pk=self.pk).filter(
                    short_url=short_str).exists():
                short_str = get_random_string()
        self.short_url = short_str

    def save(self, *args, **kwargs):
        # full_clean for validation from shell
        self.full_clean()
        super(ShortURL, self).save(*args, **kwargs)
