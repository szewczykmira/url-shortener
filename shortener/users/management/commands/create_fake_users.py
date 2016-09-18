# -*- coding: utf-8 -*-

from django.core.management import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Fetch fake users to database"

    def handle(self, *args, **options):
        self.stdout.write("Test")
