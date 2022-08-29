from django.core.management.base import BaseCommand

from wagtailthemes.models import Theme
from wagtailthemes.utils import import_theme_from_zip_file


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("theme", type=str)
        parser.add_argument("path", type=str)

    def handle(self, *args, **options):
        theme = options["theme"]
        path = options["path"]

        theme = Theme.objects.get(pathname=theme)

        import_theme_from_zip_file(theme, path)
