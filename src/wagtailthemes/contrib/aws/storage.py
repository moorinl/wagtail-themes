from storages.backends.s3boto3 import S3Boto3Storage

from wagtailthemes.settings import (
    AWS_STATIC_FILE_S3_CUSTOM_DOMAIN,
    AWS_STATIC_FILE_STORAGE_BUCKET_NAME,
)


class StaticFileS3BotoStorage(S3Boto3Storage):
    def __init__(self, **settings):
        super().__init__(
            querystring_auth=False,
            file_overwrite=True,
            default_acl="private",
            bucket_name=AWS_STATIC_FILE_STORAGE_BUCKET_NAME,
            custom_domain=AWS_STATIC_FILE_S3_CUSTOM_DOMAIN,
            **settings
        )
