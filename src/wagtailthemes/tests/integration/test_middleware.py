import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test.utils import override_settings

from wagtailthemes.thread import get_theme, set_theme


@pytest.mark.django_db
def test_middleware_not_configured(client):
    with override_settings(MIDDLEWARE=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'wagtailthemes.middleware.ThemeMiddleware',
        'wagtail.core.middleware.SiteMiddleware',
    ]):
        with pytest.raises(ImproperlyConfigured):
            client.get('/')


@pytest.mark.django_db
def test_middleware_set_theme_for_site(client, site, settings):
    settings.theme = 'personal'
    settings.save()

    set_theme('wagtail')
    assert get_theme() == 'wagtail'

    client.get('/')
    assert get_theme() == 'personal'
