from django.template.loader import get_template
from django.test.utils import override_settings

from wagtailthemes.thread import set_theme


def test_get_dirs_no_theme_set():
    set_theme(None)
    template = get_template('base.html')
    assert template.render() == 'Base'


@override_settings(WAGTAIL_THEME_PATH=None)
def test_get_dirs_no_theme_dir():
    set_theme('brand')
    template = get_template('base.html')
    assert template.render() == 'Brand Base'


@override_settings(WAGTAIL_THEME_PATH='themes')
def test_get_dirs():
    set_theme('brand')
    template = get_template('base.html')
    assert template.render() == 'Themes Brand Base'


@override_settings(WAGTAIL_THEME_PATH='themes')
def test_get_dirs_with_extend():
    set_theme('brand')
    template = get_template('page.html')
    assert template.render() == 'Page - Themes Brand Base'
