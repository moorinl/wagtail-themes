import os

from django.template.loaders.filesystem import Loader as BaseLoader

from wagtailthemes.thread import get_theme


class ThemeLoader(BaseLoader):
    def get_dirs(self):
        dirs = super(ThemeLoader, self).get_dirs()
        theme = get_theme()

        if theme:
            theme_dirs = [os.path.join(dir, theme) for dir in dirs]
            return theme_dirs

        return dirs
