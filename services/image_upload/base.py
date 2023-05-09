from abc import ABC, abstractmethod
from PIL import Image


class BaseStorageClient(ABC):
    @abstractmethod
    def upload(self, image: Image, name: str):
        pass
