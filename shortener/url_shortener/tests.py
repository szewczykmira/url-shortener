# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase

from models import ShortURL
from users.utils import get_random_user


class ShortenerTest(TestCase):
    fixtures = ['users.json']

    def test_view_home(self):
        response = self.client.get(reverse('home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'url_shortener/home.html')

    def test_model_must_have_origin_url(self):
        user = get_random_user()
        count = ShortURL.objects.all().count()
        has_error = False
        try:
            obj = ShortURL(user=user, short_url="foo")
            obj.save()
        except ValidationError:
            has_error = True

        self.assertTrue(has_error)
        self.assertEqual(count, ShortURL.objects.all().count())

    def test_model_must_have_user(self):
        count = ShortURL.objects.all().count()
        has_error = False
        try:
            obj = ShortURL(short_url="foo", original_url="bar")
            obj.save()
        except ValidationError:
            has_error = True
        self.assertTrue(has_error)
        self.assertEqual(count, ShortURL.objects.all().count())

    def test_model_must_have_short_url(self):
        user = get_random_user()
        count = ShortURL.objects.all().count()
        has_error = False
        try:
            obj = ShortURL(original_url="foo", user=user)
            obj.save()
        except ValidationError:
            has_error = True
        self.assertTrue(has_error)
        self.assertEqual(count, ShortURL.objects.all().count())