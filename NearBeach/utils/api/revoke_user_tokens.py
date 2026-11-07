from django.db import transaction
from django.db.models import Q
from knox.models import get_token_model
from oauth2_provider.models import get_access_token_model, get_grant_model, get_refresh_token_model


def revoke_user_tokens(user) -> None:
    """Cancel every API token that lets someone act as this user

    Covers Knox tokens and everything django-oauth-toolkit has issued - including the tokens of an application whose
    service user this is, as those are stored against the application rather than a person.
    """
    with transaction.atomic():
        get_token_model().objects.filter(user=user).delete()

        get_grant_model().objects.filter(user=user).delete()
        get_refresh_token_model().objects.filter(user=user).delete()
        get_access_token_model().objects.filter(
            Q(user=user) | Q(user__isnull=True, application__user=user)
        ).delete()
