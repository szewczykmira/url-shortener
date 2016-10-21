# -*- coding: utf-8 -*-

from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

import urllib2
import json

User = get_user_model()


class Command(BaseCommand):
    help = "Fetch fake users to database"

    def add_arguments(self, parser):
        parser.add_argument('people', type=int)

    def handle(self, *args, **options):
        people_number = options['people']
        data = self.extract_data(people_number)
        self.create_users(data['results'])

        self.stdout.write(self.style.SUCCESS("Fake users added!"))

    def extract_data(self, people):
        url = "http://api.randomuser.me/?results={result}" \
              "&exc=nat,picture,id,cell,phone,dob,location,gender".format(
            result=people)
        response = urllib2.urlopen(url)
        return json.load(response)

    def create_user(self, item):
        obj = {
            'first_name': item['name']['first'],
            'last_name': item['name']['last'],
            'username': item['login']['username'],
            'email': item['email'],
            'password': item['login']['password'],
            'date_joined': item['registered']
        }
        return User(**obj)

    def create_users(self, items):
        User.objects.bulk_create([self.create_user(elem) for elem in items])
