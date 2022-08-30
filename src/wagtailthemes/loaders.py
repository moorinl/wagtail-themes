import logging
import os

from django.conf import settings
from django.db.utils import ProgrammingError
from django.template import Origin, TemplateDoesNotExist
from django.template.loaders.base import Loader
from django.template.loaders.filesystem import Loader as BaseFileLoader

from wagtailthemes.cache import (
    get_and_set_template_contents_in_cache,
    get_cache_key,
    get_from_cache,
    get_not_found_cache_key,
    set_in_cache,
)
from wagtailthemes.models import Template
from wagtailthemes.thread import get_theme

logger = logging.getLogger(__name__)


class ThemeLoader(BaseFileLoader):
    """
    Theme template Loader class for serving optional themes per Wagtail site.
    """

    def get_dirs(self):
        dirs = super(ThemeLoader, self).get_dirs()
        theme = get_theme()
        theme_path = getattr(settings, "WAGTAIL_THEME_PATH", None)

        if theme:
            if theme_path:
                # Prepend theme path if WAGTAIL_THEME_PATH is set
                theme_dirs = [os.path.join(dir, theme_path, theme) for dir in dirs]
            else:
                # Append theme for each directory in the DIRS option of the
                # TEMPLATES setting
                theme_dirs = [os.path.join(dir, theme) for dir in dirs]
            return theme_dirs

        return dirs


class ModelThemeLoader(Loader):
    def get_contents(self, origin):
        theme = get_theme()
        cache_key = get_cache_key(origin.template_name, theme)

        # Try to load contents from cache first
        contents = get_from_cache(cache_key, None)
        if contents:
            return contents

        # If contents is not found, check if template is tried earlier and marked
        # already as not found (prevent database lookups)
        not_found_cache_key = get_not_found_cache_key(origin.template_name, theme)
        marked_as_not_found = get_from_cache(not_found_cache_key, None)
        if marked_as_not_found:
            raise TemplateDoesNotExist(origin)

        # Try to load the template from the database
        try:
            template = Template.objects.get(
                theme__pathname=theme, path=origin.template_name
            )
        except Template.DoesNotExist:
            # Mark the template as not found for the next time
            set_in_cache(not_found_cache_key, 1)
            raise TemplateDoesNotExist(origin)
        except ProgrammingError:
            # Skip migration errors (some apps render templates on load)
            raise TemplateDoesNotExist(origin)

        # Save the template contents in the cache
        contents = get_and_set_template_contents_in_cache(cache_key, template)
        return contents

    def get_template_sources(self, template_name):
        yield Origin(
            name=template_name,
            template_name=template_name,
            loader=self,
        )
