from django.core.management import BaseCommand

from api.views import IndexerView


class Command(BaseCommand):
    help = 'Index all the image in indexed image directory'

    def handle(self, *args, **options):
        IndexerView.get()
