# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase

from models import ShortURL
from users import utils


class ShortenerTest(TestCase):
    fixtures = ['users.json']

    def test_view_home(self):
        response = self.client.get(reverse('home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'url_shortener/home.html')

    def test_model_must_have_origin_url(self):
        user = utils.get_random_user()
        count = ShortURL.objects.all().count()
        has_error = False
        try:
            obj = ShortURL(user=user, short_url="ala")
            obj.save()
        except ValidationError:
            has_error = True

        self.assertTrue(has_error)
        self.assertEqual(count, ShortURL.objects.all().count())
