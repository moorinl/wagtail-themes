import os

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

from wagtailthemes.cache import (
    delete_from_cache,
    get_and_set_file_hash_in_cache,
    get_and_set_template_contents_in_cache,
    get_cache_key,
    get_not_found_cache_key,
    set_in_cache,
)
from wagtailthemes.storage import StaticFileField
from wagtailthemes.utils import (
    compute_file_checksum_from_file,
    compute_file_checksum_from_text,
)

__ALL__ = ["ThemeSettings", "File", "TemplateFile"]

PATH_HELP_TEXT = _(
    "The pathname of the theme which must match the pathname used in your templates."
)


class Theme(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    pathname = models.CharField(
        _("Pathname"), max_length=255, unique=True, help_text=PATH_HELP_TEXT
    )

    created = models.DateTimeField(_("Created"), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_("Modified"), auto_now=True, editable=False)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("pathname"),
            ],
            heading=_("Theme"),
        )
    ]

    class Meta:
        ordering = ["name"]
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")

    def __str__(self):
        return self.name


class File(models.Model):
    theme = models.ForeignKey(
        "wagtailthemes.Theme",
        verbose_name=_("Theme"),
        on_delete=models.CASCADE,
        related_name="+",
    )
    path = models.TextField(_("Path"))
    hash = models.TextField(_("Hash"), editable=False, null=True, blank=False)

    created = models.DateTimeField(_("Created"), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_("Modified"), auto_now=True, editable=False)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Modified by"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        abstract = True
        ordering = ["path"]
        unique_together = ["theme", "path"]

    def __str__(self):
        return self.path


class Template(File):
    value = models.TextField(_("Value"))

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("theme"),
                FieldPanel("path"),
            ],
            heading=_("Template"),
        ),
        FieldPanel("value"),
    ]

    class Meta:
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")
        unique_together = ["theme", "path"]

    def save(self, *args, **kwargs):
        self.hash = compute_file_checksum_from_text(self.value)
        super().save(*args, **kwargs)


class StaticFile(File):
    file = StaticFileField(_("File"))

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("theme"),
                FieldPanel("path"),
            ],
            heading=_("Template"),
        ),
        FieldPanel("file"),
    ]

    class Meta:
        verbose_name = _("Static file")
        verbose_name_plural = _("Static files")
        unique_together = ["theme", "path"]

    @property
    def location(self):
        return os.path.join(self.theme.pathname, self.path)

    def save(self, *args, **kwargs):
        self.hash = compute_file_checksum_from_file(self.file)
        super().save(*args, **kwargs)


@register_setting
class ThemeSettings(BaseSetting):
    id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
    )
    theme = models.ForeignKey(
        "wagtailthemes.Theme",
        verbose_name=_("Theme"),
        on_delete=models.CASCADE,
        null=True,
        blank=False,
        related_name="+",
    )

    panels = [
        FieldPanel("theme"),
    ]

    class Meta:
        verbose_name = _("themes")
        verbose_name_plural = _("themes")


@receiver(post_delete, sender=Template)
def delete_template_cache_and_mark_as_not_found(sender, instance, **kwargs):
    # Clear the template cache
    cache_key = get_cache_key(instance.path, instance.theme.pathname)
    delete_from_cache(cache_key)

    # Mark the template as not found
    not_found_cache_key = get_not_found_cache_key(
        instance.path, instance.theme.pathname
    )
    set_in_cache(not_found_cache_key, 1)


@receiver(post_save, sender=Template)
def update_template_cache(sender, instance, **kwargs):
    # Save the template contents in the cache
    cache_key = get_cache_key(instance.path, instance.theme.pathname)
    get_and_set_template_contents_in_cache(cache_key, instance)

    # Make sure the template is not marked as not found
    not_found_cache_key = get_not_found_cache_key(
        instance.path, instance.theme.pathname
    )
    delete_from_cache(not_found_cache_key)


@receiver(post_delete, sender=StaticFile)
def delete_static_file_cache_and_mark_as_not_found(sender, instance, **kwargs):
    # Clear the static file cache
    cache_key = get_cache_key(instance.path, instance.theme.pathname)
    delete_from_cache(cache_key)

    # Mark the static file as not found
    not_found_cache_key = get_not_found_cache_key(
        instance.path, instance.theme.pathname
    )
    set_in_cache(not_found_cache_key, 1)


@receiver(post_save, sender=StaticFile)
def update_static_file_cache(sender, instance, **kwargs):
    # Save the static file hash in the cache
    cache_key = get_cache_key(instance.path, instance.theme.pathname)
    get_and_set_file_hash_in_cache(cache_key, instance)

    # Make sure the static file is not marked as not found
    not_found_cache_key = get_not_found_cache_key(
        instance.path, instance.theme.pathname
    )
    delete_from_cache(not_found_cache_key)
