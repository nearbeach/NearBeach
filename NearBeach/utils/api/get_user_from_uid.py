from django.contrib.auth.models import User
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


def get_user_from_uid(uid: str) -> User | None:
    """Get the active user a password reset link was made for.

    The uid comes straight from the url, so anything can arrive - bad base64, bytes that are not text,
    or text that is not a user id. All of those are "no such user", never an error.
    """
    try:
        user_id = int(force_str(urlsafe_base64_decode(uid)))
    except (ValueError, TypeError, OverflowError, UnicodeDecodeError):
        return None

    return User.objects.filter(
        pk=user_id,
        is_active=True,
    ).first()
