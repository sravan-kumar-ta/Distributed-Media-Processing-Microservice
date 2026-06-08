import json

from app.services.redis_service import redis_client


class FileService:
    PREFIX = "file"

    def _key(self, file_id: str):
        return f"{self.PREFIX}:{file_id}"

    def save_file_metadata(
        self,
        file_id: str,
        storage_key: str,
        original_filename: str,
    ):
        data = {
            "file_id": file_id,
            "storage_key": storage_key,
            "original_filename": original_filename,
        }

        redis_client.set(self._key(file_id), json.dumps(data))

    def get_file_metadata(self, file_id: str):
        data = redis_client.get(self._key(file_id))

        if not data:
            return None

        return json.loads(data)


file_service = FileService()
