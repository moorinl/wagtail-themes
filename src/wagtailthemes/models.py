from django import forms
from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import register_setting

if WAGTAIL_VERSION < (4, 0):
    from wagtail.contrib.settings.models import BaseSetting
else:
    from wagtail.contrib.settings.models import BaseSiteSetting as BaseSetting

__ALL__ = ["ThemeSettings"]


@register_setting
class ThemeSettings(BaseSetting):
    THEMES = getattr(settings, "WAGTAIL_THEMES", None)

    id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
    )
    theme = models.CharField(blank=True, max_length=255, null=True)

    panels = [FieldPanel("theme", widget=forms.Select(choices=THEMES))]

    class Meta:
        verbose_name = _("themes")
        verbose_name_plural = _("themes")
