from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin

from wagtailthemes.models import ThemeSettings
from wagtailthemes.thread import set_theme


class ThemeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.site:
            raise ImproperlyConfigured(
                "ThemeMiddleware must be added after SiteMiddleware")

        theme_settings = ThemeSettings.for_site(request.site)
        theme = theme_settings.theme

        if theme:
            set_theme(theme)
