import logging

from firebase_admin.auth import InvalidIdTokenError
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from authentication.models import User
from authentication.utils import verify_token

logger = logging.getLogger(__name__)


class FirebaseAuthentication(BasePermission):
    def has_permission(self, request: Request, view):
        id_token = request.headers.get('Authorization', '').split(' ').pop()
        try:
            uuid = verify_token(id_token)
            if not uuid:
                return False

            user = User.objects.get(firebase_user_id=uuid)
            request.user = user
            return True
        except Exception as e:
            logger.error('Error while checking user permission:', e)
            return False


class AnonymousOrAuthorized(FirebaseAuthentication):
    def has_permission(self, request: Request, view):
        super().has_permission(request, view)

        return True
