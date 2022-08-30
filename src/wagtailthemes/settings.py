from django.conf import settings


def get_setting(name: str, default=None):
    return getattr(settings, "WAGTAIL_THEMES_%s" % name, default)


CACHE_KEY_PREFIX = get_setting("CACHE_KEY_PREFIX", default="wagtailthemes")
IGNORE_FILES_FROM_IMPORT = get_setting(
    "IGNORE_FILES_FROM_IMPORT", default=[".DS_Store"]
)
STATIC_ROOT = get_setting("STATIC_ROOT", default=settings.MEDIA_ROOT)
STATIC_URL = get_setting("STATIC_URL", default=settings.MEDIA_URL)
VERSIONING = get_setting("VERSIONING", default=True)
DEFAULT_STATIC_FILE_STORAGE = get_setting(
    "DEFAULT_STATIC_FILE_STORAGE", default="wagtailthemes.storage.StaticFilesStorage"
)
AWS_STATIC_FILE_STORAGE_BUCKET_NAME = get_setting(
    "AWS_STATIC_FILE_STORAGE_BUCKET_NAME", default=""
)
AWS_STATIC_FILE_S3_CUSTOM_DOMAIN = get_setting(
    "AWS_STATIC_FILE_S3_CUSTOM_DOMAIN", default=""
)
