import getpass
from django.utils.termcolors import make_style
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from catalogue.services import preload_materials_catalogue, preload_work_catalogue

INFO_STYLE = blue_style = make_style(fg="blue", opts=("bold",))


class Command(BaseCommand):
    help = "Loads a CSV file of starter items into the catalogue for a user."

    def add_arguments(self, parser):
        # Positional argument (required)
        parser.add_argument('user', type=str, help='The username of the user')

    def handle(self, *args, **options):
        username = options['user']
        user = User.objects.filter(username=username).first()
        if not user:
            create_user = input("User not found, create it? [y/n]: ").strip()
            if create_user.lower() == 'y':
                passwords_match = False
                password = None
                confirm_password = None
                while not passwords_match:
                    password = getpass.getpass("Enter password: ")
                    confirm_password = getpass.getpass("Confirm password: ")

                    passwords_match = password == confirm_password

                    if not passwords_match:
                        self.stdout.write(self.style.ERROR("Password doesn't match."))

                self.stdout.write(self.style.SUCCESS("Passwords match."))
                is_super = input("Make them a superuser? [y/n]: ").strip()

                if is_super.lower() == 'y':
                    user = User.objects.create_superuser(
                        username=username,
                        email=username,
                        password=password
                    )
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=username,
                        password=password
                    )

                self.stdout.write(self.style.SUCCESS("User created."))

            else:
                self.stdout.write(self.style.ERROR("No user found."))

        self.stdout.write(INFO_STYLE("Creating catalogue."))
        preload_materials_catalogue(user=user, flush=True)
        preload_work_catalogue(user=user, flush=True)
        self.stdout.write(self.style.SUCCESS("Done."))
