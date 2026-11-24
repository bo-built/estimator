from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from catalogue.services import preload_starter_catalogue


class Command(BaseCommand):
    help = "Loads a CSV file of starter items into the catalogue for a user."

    def add_arguments(self, parser):
        # Positional argument (required)
        parser.add_argument('user', type=int, help='The integer ID of the user')

    def handle(self, *args, **options):
        user_id = options['user']
        user = User.objects.get(pk=user_id)
        preload_starter_catalogue(user=user, flush=True)
