from django.core.management import call_command
from django.test import TestCase

from .models import Author, Book, Member


class SeedDemoDataTests(TestCase):
    def test_command_is_repeatable(self):
        call_command("seed_demo_data", stdout=None)
        call_command("seed_demo_data", stdout=None)

        self.assertEqual(Author.objects.count(), 3)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Member.objects.count(), 2)
