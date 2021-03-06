# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase

from .models import ShortURL
from .forms import ShortURLForm
from .utils import get_random_string
from users.utils import get_random_user

import base64


class ShortenerTest(TestCase):
    fixtures = ['users.json']

    def test_model_must_have_origin_url(self):
        user = get_random_user()
        count = ShortURL.objects.all().count()
        with self.assertRaises(ValidationError):
            obj = ShortURL(user=user, short_url="foo")
            obj.save()

        self.assertEqual(count, ShortURL.objects.all().count())

    def test_model_must_have_user(self):
        count = ShortURL.objects.all().count()
        with self.assertRaises(ValidationError):
            obj = ShortURL(short_url="foo", original_url="http://www.bar.com")
            obj.save()
        self.assertEqual(count, ShortURL.objects.all().count())

    def test_model_must_have_short_url(self):
        count = ShortURL.objects.all().count()
        with self.assertRaises(ValidationError):
            obj = ShortURL(original_url="http://www.foo.com",
                           user=get_random_user())
            obj.save()

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

    def test_short_url_form_valid_data(self):
        form = ShortURLForm({'original_url': 'http://google.com'})
        self.assertTrue(form.is_valid())
        obj = form.save()
        self.assertEqual(obj.original_url, 'http://google.com')

    def test_short_url_form_no_data(self):
        form = ShortURLForm()
        self.assertFalse(form.is_valid())

    def test_short_url_form_not_valid(self):
        form = ShortURLForm({'original_url': 'foo'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'original_url': [u"Enter a valid URL."]})

    def test_view_home_get(self):
        response = self.client.get(reverse('home'), follow=True)
        context = response.context[-1]
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(context['form'], ShortURLForm))
        self.assertTemplateUsed(response, 'url_shortener/home.html')

    def test_view_home_post(self):
        obj = ShortURL(original_url="http://foo.com",
                       short_url="bar", user=get_random_user())
        obj.save()
        count = ShortURL.objects.all()

    def test_follow_link(self):
        response = self.client.get(reverse('follow_link',
                                           kwargs={'short_url': 'foo'}))
        self.assertRedirects(response, '/')
        obj = ShortURL(original_url="http://foo.com",
                       short_url="bar", user=get_random_user())
        obj.save()
        response_true = self.client.get(
            reverse('follow_link', kwargs={'short_url': 'bar'}))
        self.assertRedirects(response_true, 'http://foo.com',
                            target_status_code=302)

    def test_display_info_not_exists(self):
        response = self.client.get(reverse('display_info',
                                           kwargs={'short_url': 'foo'}))
        self.assertRedirects(response, '/')

    def test_display_info_exists(self):
        obj = ShortURL(original_url="http://foo.com",
                       short_url="bar", user=get_random_user())
        obj.save()
        response = self.client.get(
            reverse('display_info', kwargs={'short_url': 'bar'}), follow=True)
        context = response.context[-1]
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(context['object'], ShortURL))
        self.assertTemplateUsed(response, 'url_shortener/display_info.html')

    def home_use_existing_url(self):
        obj = ShortURL(original_url="http://foo.com",
                       short_url="bar", user=get_random_user())
        obj.save()
        response = self.client.post(reverse('home'),
                                    {'original_url': 'http:foo.com'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/!bar', status_code=200)

    def test_home_create_url(self):
        reponse = self.client.post(reverse('home'),
                                   {'orignal_url': 'http://google.com'},
                                   follow=True)
        self.assertEqual(reponse.status_code, 200)
