import os

from django.conf import settings
from django.template.loaders.filesystem import Loader as BaseLoader

from wagtailthemes.thread import get_theme


class ThemeLoader(BaseLoader):
    """
    Theme template Loader class for serving optional themes per Wagtail site.
    """
    def get_dirs(self):
        dirs = super(ThemeLoader, self).get_dirs()
        theme = get_theme()
        theme_path = getattr(settings, 'WAGTAIL_THEME_PATH', None)

        if theme:
            if theme_path:
                # Prepend theme path if WAGTAIL_THEME_PATH is set
                theme_dirs = [
                        os.path.join(dir, theme_path, theme) for dir in dirs]
            else:
                # Append theme for each directory in the DIRS option of the
                # TEMPLATES setting
                theme_dirs = [os.path.join(dir, theme) for dir in dirs]
            return theme_dirs

        return dirs
