# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase

from .models import ShortURL
from .utils import get_random_string
from users.utils import get_random_user

import base64


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
        count = ShortURL.objects.all().count()
        has_error = False
        try:
            obj = ShortURL(original_url="http://www.foo.com",
                           user=get_random_user())
            obj.save()
        except ValidationError:
            has_error = True
        self.assertTrue(has_error)
        self.assertEqual(count, ShortURL.objects.all().count())

    def test_model_add(self):
        count = ShortURL.objects.all().count()
        has_error = False
        obj = ShortURL(original_url="http://foo.com",
                       short_url="bar", user=get_random_user())
        obj.save()

        self.assertFalse(has_error)
        self.assertEqual(count + 1, ShortURL.objects.all().count())

    def test_get_random_string(self):
        random_string = get_random_string()
        self.assertTrue(len(random_string) <= settings.SHORT_URL_MAX_LEN)
        self.assertTrue(random_string)

    def test__str_(self):
        obj = ShortURL(original_url="http://foo.com", user=get_random_user(),
                       short_url="bar")
        obj.save()
        self.assertEqual(str(obj), "http://foo.com")

    def test_set_short_url_short(self):
        google_base64 = base64.urlsafe_b64encode("http://google.com")
        obj = ShortURL(original_url="http://google.com", user=get_random_user())
        obj.set_short_url()
        obj.save()
        self.assertEqual(google_base64, obj.short_url)

    def test_set_short_url_long(self):
        long_url = "https://www.google.pl/?gfe_rd=cr&ei=gb_iV7D5D8mv8weqp53" \
                   "YDQ#q=lorem+ipsum+dolor+sit+amet+enim.+etiam+ullamcorper" \
                   ".+suspendisse+a+pellentesque+dui+non+felis"
        base64_str = base64.urlsafe_b64encode(long_url)
        obj = ShortURL(original_url=long_url, user=get_random_user())
        with self.settings(SHORT_URL_MAX_LEN=50):
            obj.set_short_url()
        obj.save()
        self.assertNotEqual(base64_str, obj.short_url)
