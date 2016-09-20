# -*- coding: utf-8 -*-

from django import forms
from .models import ShortURL


class ShortURLForm(forms.ModelForm):
    """
    Class for form which create instance of ShortURL model
    """
    class Meta:
        model = ShortURL
        fields = ['original_url']
