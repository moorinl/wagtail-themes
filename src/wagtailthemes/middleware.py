from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin
from wagtail.core.models import Site

from wagtailthemes.models import ThemeSettings
from wagtailthemes.thread import set_theme


class ThemeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        site = Site.find_for_request(request)

        if not site:
            raise ImproperlyConfigured(
                "Site not found!")

        theme_settings = ThemeSettings.for_site(site)
        theme = theme_settings.theme

        if theme:
            set_theme(theme)
