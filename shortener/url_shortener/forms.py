# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from .models import ShortURL
from users.utils import get_random_user

User = get_user_model()


class ShortURLForm(forms.ModelForm):
    """
    Class for form which create instance of ShortURL model
    """
    class Meta:
        model = ShortURL
        fields = ['original_url']

    def save(self, *args, **kwargs):
        obj = super(ShortURLForm, self).save(commit=False)
        obj.user = get_random_user()
        obj.set_short_url()
        obj.save()
        return obj
