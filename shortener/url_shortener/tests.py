# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase

from .models import ShortURL
from .utils import get_random_string
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
            obj = ShortURL(short_url="foo", original_url="http://www.bar.com")
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
            obj = ShortURL(original_url="http://www.foo.com", user=user)
            obj.save()
        except ValidationError:
            has_error = True
        self.assertTrue(has_error)
        self.assertEqual(count, ShortURL.objects.all().count())

    def test_model_add(self):
        user = get_random_user()
        count = ShortURL.objects.all().count()
        has_error = False
        obj = ShortURL(original_url="http://foo.com",
                       short_url="bar", user=user)
        obj.save()

        self.assertFalse(has_error)
        self.assertEqual(count + 1, ShortURL.objects.all().count())

    def test_get_random_string(self):
        random_string = get_random_string()
        self.assertTrue(len(random_string) <= settings.SHORT_URL_MAX_LEN)
        self.assertTrue(random_string)
