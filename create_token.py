from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Create a token for a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username of the user to create a token for')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"The user '{username}' does not exist."))
            return
        token, created = Token.objects.get_or_create(user=user)
        if created:
            self.stdout.write(self.style.SUCCESS(f"A new token has been created for user '{username}': {token.key}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"A token already exists for user '{username}': {token.key}"))
