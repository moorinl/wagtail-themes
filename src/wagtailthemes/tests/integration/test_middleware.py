import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test.utils import override_settings
from wagtail.core.models import Site

from wagtailthemes.thread import get_theme, set_theme


@pytest.mark.django_db
def test_middleware_no_site(client):
    with override_settings(
        MIDDLEWARE=[
            "wagtailthemes.middleware.ThemeMiddleware",
        ]
    ):
        # Remove all sites to simulate not being able to find the site.
        Site.objects.all().delete()
        with pytest.raises(ImproperlyConfigured):
            client.get("/")


@pytest.mark.django_db
def test_middleware_set_theme_for_site(client, site, settings):
    settings.theme = "personal"
    settings.save()

    set_theme("wagtail")
    assert get_theme() == "wagtail"

    client.get("/")
    assert get_theme() == "personal"
