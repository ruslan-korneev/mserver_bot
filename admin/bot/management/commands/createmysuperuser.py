from django.core.management.base import BaseCommand    

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('password')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        return u'Username: %s  Password: %s' % (username, password)
