from wagtailthemes.cache import get_cache_key, get_not_found_cache_key


def test_get_cache_key():
    assert get_cache_key("base.html") == "wagtailthemes:basehtml"
    assert get_cache_key("cms/pages/home.html") == "wagtailthemes:cmspageshomehtml"
    assert (
        get_cache_key("cms/pages/home.html", "my-theme")
        == "wagtailthemes:my-theme:cmspageshomehtml"
    )


def test_not_found_cache_key():
    assert (
        get_not_found_cache_key("cms/pages/home.html", "my-theme")
        == "wagtailthemes:my-theme:cmspageshomehtml:notfound"
    )
