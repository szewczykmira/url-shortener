# -*- coding: utf-8 -*-

from django.core.management import call_command, CommandError
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.six import StringIO

User = get_user_model()


class CreateFakeUsersTest(TestCase):

    def setUp(self):
        self.out = StringIO()

    def test_no_arguments(self):
        error_rise = False
        try:
            call_command('create_fake_users', stdout=self.out)
        except CommandError:
            error_rise = True
        self.assertTrue(error_rise)

    def test_wrong_argument_type(self):
        error_rise = False
        try:
            call_command('create_fake_users', "wq", stdout=self.out)
        except CommandError:
            error_rise = True
        self.assertTrue(error_rise)

    def test_string_as_int(self):
        try:
            call_command("create_fake_users", "12", stdout=self.out)
            error_rise = False
        except CommandError:
            error_rise = True
        self.assertFalse(error_rise)

    def test_create_users(self):
        count = User.objects.all().count()
        people = 12
        call_command('create_fake_users', people, stdout=self.out)
        self.assertEqual(count + people, User.objects.all().count())
