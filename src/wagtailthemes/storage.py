import os

from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage
from django.db.models import FileField
from django.utils.deconstruct import deconstructible
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string

from wagtailthemes.settings import DEFAULT_STATIC_FILE_STORAGE, STATIC_ROOT, STATIC_URL


@deconstructible
class StaticFilesStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if location is None:
            location = STATIC_ROOT
        if base_url is None:
            base_url = STATIC_URL

        super().__init__(location, base_url, *args, **kwargs)
        # FileSystemStorage fallbacks to MEDIA_ROOT when location
        # is empty, so we restore the empty value.
        if not location:
            self.base_location = None
            self.location = None

    def path(self, name):
        if not self.location:
            raise ImproperlyConfigured(
                "You're using the wagtailthemes app "
                "without having set the STATIC_ROOT "
                "setting to a filesystem path."
            )
        return super().path(name)


def get_static_file_storage_class(import_path=None):
    return import_string(import_path or DEFAULT_STATIC_FILE_STORAGE)


class DefaultStaticFileStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_static_file_storage_class()()


default_static_file_storage = DefaultStaticFileStorage()


def static_file_path(instance, filename):
    return os.path.join(instance.theme.pathname, instance.path)


class StaticFileField(FileField):
    def __init__(
        self,
        verbose_name=None,
        name=None,
        upload_to=static_file_path,
        storage=None,
        **kwargs
    ):
        self.storage = default_static_file_storage
        if callable(self.storage):
            # Hold a reference to the callable for deconstruct().
            self._storage_callable = self.storage
            self.storage = self.storage()
        super().__init__(
            verbose_name=verbose_name,
            name=name,
            upload_to=upload_to,
            storage=storage,
            **kwargs
        )
