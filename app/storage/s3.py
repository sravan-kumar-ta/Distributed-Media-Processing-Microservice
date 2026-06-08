import boto3

from app.core.config import settings
from app.storage.base import StorageProvider


class S3Storage(StorageProvider):
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )

    def upload(self, local_path: str, object_key: str):
        self.client.upload_file(
            local_path,
            settings.aws_bucket_name,
            object_key,
        )

    def download(self, object_key: str, local_path: str):
        self.client.download_file(
            settings.aws_bucket_name,
            object_key,
            local_path,
        )
    
    def exists(self, object_key):
        try:
            self.client.head_object(
                Bucket=settings.aws_bucket_name,
                Key=object_key,
            )

            return True

        except Exception:

            return False
