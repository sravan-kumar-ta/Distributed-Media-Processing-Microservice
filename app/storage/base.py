from abc import ABC
from abc import abstractmethod


class StorageProvider(ABC):

    @abstractmethod
    def upload(self, local_path: str, object_key: str):
        pass

    @abstractmethod
    def download(self, object_key: str, local_path: str):
        pass

    @abstractmethod
    def exists(self, object_key: str) -> bool:
        pass
