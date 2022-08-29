from django.core.cache import cache
from django.template.defaultfilters import slugify

from wagtailthemes.settings import CACHE_KEY_PREFIX


def get_cache_key(name, theme=None):
    cache_key = slugify(name)
    if theme:
        cache_key = theme + ":" + cache_key
    return CACHE_KEY_PREFIX + ":" + cache_key


def get_not_found_cache_key(name, theme=None):
    cache_key = get_cache_key(name, theme)
    cache_key += ":" + "notfound"
    return cache_key


def get_from_cache(cache_key, default=None):
    return cache.get(cache_key, default)


def set_in_cache(cache_key, value):
    cache.set(cache_key, value)


def get_and_set_template_contents_in_cache(cache_key, template):
    value = template.value
    set_in_cache(cache_key, value)
    return value


def get_and_set_file_hash_in_cache(cache_key, file):
    hash = file.hash
    set_in_cache(cache_key, hash)
    return hash


def delete_from_cache(cache_key):
    cache.delete(cache_key)
