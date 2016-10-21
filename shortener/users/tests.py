# -*- coding: utf-8 -*-

from django.core.management import call_command, CommandError
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.six import StringIO

from .utils import get_random_user

User = get_user_model()


class CreateFakeUsersTest(TestCase):

    def setUp(self):
        self.out = StringIO()

    def test_no_arguments(self):
        with self.assertRaises(CommandError):
            call_command('create_fake_users', stdout=self.out)

    def test_wrong_argument_type(self):
        with self.assertRaises(CommandError):
            call_command('create_fake_users', "wq", stdout=self.out)

    def test_create_users(self):
        count = User.objects.all().count()
        people = 12
        call_command('create_fake_users', people, stdout=self.out)
        self.assertEqual(count + people, User.objects.all().count())

    def test_random_users_no_users(self):
        with self.assertRaises(User.DoesNotExist):
            get_random_user()

    def test_get_random_users(self):
        call_command('create_fake_users', 12, stdout=self.out)
        random_user = get_random_user()
        self.assertTrue(isinstance(random_user, User))
