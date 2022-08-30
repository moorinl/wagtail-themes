import os

from django import template
from django.db.utils import ProgrammingError
from django.templatetags.static import StaticNode

from wagtailthemes.cache import (
    get_and_set_file_hash_in_cache,
    get_cache_key,
    get_from_cache,
    get_not_found_cache_key,
    set_in_cache,
)
from wagtailthemes.models import StaticFile
from wagtailthemes.settings import VERSIONING
from wagtailthemes.storage import default_static_file_storage
from wagtailthemes.thread import get_theme

register = template.Library()


class StaticThemeNode(StaticNode):
    @classmethod
    def handle_simple(cls, path):
        theme = get_theme()
        theme_path = os.path.join(theme, path)

        if VERSIONING:
            cache_key = get_cache_key(path, theme)

            # Try to load hash from cache first
            hash = get_from_cache(cache_key, None)
            if hash:
                return "%s?v=%s" % (
                    default_static_file_storage.url(theme_path),
                    hash,
                )

            # If hash is not found, check if static file is tried earlier and marked
            # already as not found (prevent database lookups)
            not_found_cache_key = get_not_found_cache_key(path, theme)
            marked_as_not_found = get_from_cache(not_found_cache_key, None)
            if marked_as_not_found:
                return default_static_file_storage.url(theme_path)

            # Try to load the hash from the database
            try:
                static_file = StaticFile.objects.get(theme__pathname=theme, path=path)
            except StaticFile.DoesNotExist:
                # Mark the hash as not found for the next time
                set_in_cache(not_found_cache_key, 1)
                return default_static_file_storage.url(theme_path)
            except ProgrammingError:
                # Skip migration errors (some apps render templates on load)
                return default_static_file_storage.url(theme_path)

            # Save the hash in the cache
            hash = get_and_set_file_hash_in_cache(cache_key, static_file)
            return "%s?v=%s" % (
                default_static_file_storage.url(theme_path),
                hash,
            )

        return default_static_file_storage.url(theme_path)


@register.tag("static_theme")
def do_static_theme(parser, token):
    """
    Join the given path with the WAGTAIL_THEMES_STATIC_URL setting and path to the
    active theme.

    Usage::

        {% static_theme path [as varname] %}

    Examples::

        {% static_theme "myapp/css/base.css" %}
        {% static_theme variable_with_path %}
        {% static_theme "myapp/css/base.css" as admin_base_css %}
        {% static_theme variable_with_path as varname %}
    """
    return StaticThemeNode.handle_token(parser, token)


def static_theme(path):
    return StaticThemeNode.handle_simple(path)
