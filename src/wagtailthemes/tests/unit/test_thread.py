from wagtailthemes.thread import get_theme, set_theme


def test_get_theme():
    # Check when no theme is set
    set_theme(None)
    assert not get_theme()

    # Check when theme is set
    set_theme('brand')
    assert get_theme() == 'brand'

    # Check when theme is overridden
    set_theme('personal')
    assert get_theme() == 'personal'
