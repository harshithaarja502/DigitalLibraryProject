import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the configured Django superuser if it does not exist."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")

        if not username or not email or not password:
            raise CommandError(
                "Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, "
                "and DJANGO_SUPERUSER_PASSWORD to provision the admin account."
            )

        user_model = get_user_model()
        existing_user = user_model._default_manager.filter(
            **{user_model.USERNAME_FIELD: username}
        ).first()
        if existing_user:
            if not existing_user.is_superuser:
                raise CommandError(
                    f"User '{username}' already exists but is not a superuser."
                )
            self.stdout.write("Configured admin account already exists.")
            return

        user_model._default_manager.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS("Admin account created."))
