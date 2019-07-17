import pytest
from django.test import Client
from wagtail.core.models import Page, Site

from wagtailthemes.models import ThemeSettings


@pytest.fixture
def page():
    page = Page.objects.get(slug='home')
    return page


@pytest.fixture
def site():
    site = Site.objects.get(is_default_site=True)
    return site


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def settings(site):
    settings = ThemeSettings.for_site(site)
    return settings
