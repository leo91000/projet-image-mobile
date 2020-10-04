from django.core.management import BaseCommand

from api.image_features_extraction import ImageFeatureExtraction
from api.views import IndexerView


class Command(BaseCommand):
    help = "Show the CNN summary"

    def handle(self, *args, **options):
        ImageFeatureExtraction.get_summary()
