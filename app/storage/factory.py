from app.storage.local import LocalStorage
from app.storage.s3 import S3Storage

USE_LOCAL_STORAGE = True


def get_storage():
    if USE_LOCAL_STORAGE:
        return LocalStorage()

    return S3Storage()
