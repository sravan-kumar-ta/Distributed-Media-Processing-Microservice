import boto3

from app.core.config import settings


class S3Service:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )

    def upload_file(self, file_path: str, object_key: str):
        self.client.upload_file(
            file_path,
            settings.aws_bucket_name,
            object_key,
        )

    def download_file(self, object_key: str, local_path: str):
        self.client.download_file(
            settings.aws_bucket_name,
            object_key,
            local_path,
        )
