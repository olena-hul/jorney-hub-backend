from firebase_admin import auth
import logging

logger = logging.getLogger(__name__)


def verify_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        logger.error('Invalid token:', e)
        return False
