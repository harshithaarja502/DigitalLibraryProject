from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from .models import Author, Book, Member


class SeedDemoDataTests(TestCase):
    def test_command_is_repeatable(self):
        call_command("seed_demo_data", stdout=None)
        call_command("seed_demo_data", stdout=None)

        self.assertEqual(Author.objects.count(), 3)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Member.objects.count(), 2)


class EnsureAdminTests(TestCase):
    @patch.dict(
        "os.environ",
        {
            "DJANGO_SUPERUSER_USERNAME": "libraryadmin",
            "DJANGO_SUPERUSER_EMAIL": "libraryadmin@example.com",
            "DJANGO_SUPERUSER_PASSWORD": "test-password",
        },
    )
    def test_command_creates_superuser_once(self):
        call_command("ensure_admin")
        user = get_user_model().objects.get(username="libraryadmin")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("test-password"))

        call_command("ensure_admin")
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertTrue(user.check_password("test-password"))

        with patch.dict(
            "os.environ",
            {"DJANGO_SUPERUSER_PASSWORD": "updated-test-password"},
        ):
            call_command("ensure_admin", "--reset-password")
        user.refresh_from_db()
        self.assertTrue(user.check_password("updated-test-password"))

    @patch.dict("os.environ", {}, clear=True)
    def test_command_requires_credentials(self):
        with self.assertRaises(CommandError):
            call_command("ensure_admin")
