from django.conf import settings
from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting


__ALL__ = ['ThemeSettings']

@register_setting
class ThemeSettings(BaseSetting):
    THEMES = getattr(settings, 'WAGTAIL_THEMES', None)

    theme = models.CharField(
        blank=True, choices=THEMES, max_length=255, null=True)
