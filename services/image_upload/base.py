from abc import ABC, abstractmethod


class BaseStorageClient(ABC):
    @abstractmethod
    def upload(self, image, name: str):
        pass
