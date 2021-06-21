from django import forms
from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

__ALL__ = ['ThemeSettings']


@register_setting
class ThemeSettings(BaseSetting):
    THEMES = getattr(settings, 'WAGTAIL_THEMES', None)

    theme = models.CharField(blank=True, max_length=255, null=True)

    panels = [
        FieldPanel('theme', widget=forms.Select(choices=THEMES))
    ]

    class Meta:
        verbose_name = _('themes')
        verbose_name_plural = _('themes')
