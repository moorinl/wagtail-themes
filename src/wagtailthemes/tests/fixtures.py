import pytest
from wagtail.wagtailcore.models import Page, Site


@pytest.fixture
def page():
    page = Page.objects.get(slug='home')
    return page


@pytest.fixture
def site():
    site = Site.objects.get(is_default_site=True)
    return site
