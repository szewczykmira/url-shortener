# -*- coding: utf-8 -*-
from django.core.urlresolvers import  reverse
from django.test import TestCase


class ShortenerTest(TestCase):
    def test_view_home(self):
        response = self.client.get(reverse('home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'url_shortener/home.html')