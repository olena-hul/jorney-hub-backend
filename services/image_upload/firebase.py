import logging
from typing import Optional

from django.conf import settings
from firebase_admin import storage

from .base import BaseStorageClient

logger = logging.getLogger(__name__)


class FirebaseStorageClient(BaseStorageClient):
    def __init__(self):
        self.bucket = storage.bucket(settings.STORAGE_BUCKET_NAME)

    def upload(self, image, name: str) -> Optional[str]:
        try:
            blob = self.bucket.blob(name)
            blob.upload_from_string(image.read(), content_type="image/png")
            blob.make_public()
            return blob.public_url
        except Exception as e:
            logger.error(f'An exception occurred while uploading image {name}: {e}')
