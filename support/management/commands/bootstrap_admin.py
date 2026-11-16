"""Initialize the first NorthStar application administrator."""

from getpass import getpass

from django.contrib.auth.forms import UserCreationForm
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from support.models import UserProfile


class Command(BaseCommand):
    help = "Create the initial NorthStar administrator."

    def handle(self, *args, **options):
        if UserProfile.objects.filter(role="administrator").exists():
            raise CommandError(
                "A NorthStar administrator already exists. "
                "Use User Management for additional accounts."
            )

        try:
            username = input("Administrator username: ").strip()
            password = getpass("Administrator password: ")
            confirmation = getpass("Confirm password: ")
        except (EOFError, KeyboardInterrupt) as exc:
            raise CommandError("Administrator creation cancelled.") from exc

        form = UserCreationForm(
            data={
                "username": username,
                "password1": password,
                "password2": confirmation,
            }
        )
        if not form.is_valid():
            raise CommandError(
                "Administrator creation failed:\n" + form.errors.as_text()
            )

        with transaction.atomic():
            user = form.save()
            UserProfile.objects.create(user=user, role="administrator")

        self.stdout.write(
            self.style.SUCCESS(
                f"NorthStar administrator '{user.username}' created successfully."
            )
        )
