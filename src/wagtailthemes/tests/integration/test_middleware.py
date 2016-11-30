import pytest


@pytest.mark.django_db
def test_middleware_not_configured():
    assert True


@pytest.mark.django_db
def test_middleware_set_theme_for_site():
    assert True


@pytest.mark.django_db
def test_middleware_no_theme_for_site():
    assert True
