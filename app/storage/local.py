from pathlib import Path
import shutil

from app.storage.base import StorageProvider


class LocalStorage(StorageProvider):
    ROOT = Path("storage")

    def upload(self, local_path: str, object_key: str):
        destination = self.ROOT / object_key
        destination.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy(local_path, destination)

    def download(self, object_key: str, local_path: str):
        source = self.ROOT / object_key

        shutil.copy(source, local_path)

    def exists(self, object_key: str):
        return (self.ROOT / object_key).exists()
