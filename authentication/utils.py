from firebase_admin import auth
import logging

from firebase_admin.auth import InvalidIdTokenError

logger = logging.getLogger(__name__)


def verify_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return uid
    except InvalidIdTokenError as e:
        if 'Token used too early' in e:
            return verify_token(token)
    except Exception as e:
        logger.error('Invalid token:', e)
        return False
