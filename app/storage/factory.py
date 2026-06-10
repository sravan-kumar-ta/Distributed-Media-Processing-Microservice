from app.storage.local import LocalStorage
from app.storage.s3 import S3Storage

from app.core.config import settings

USE_LOCAL_STORAGE = settings.use_local_storage


def get_storage():
    if USE_LOCAL_STORAGE:
        return LocalStorage()

    return S3Storage()
