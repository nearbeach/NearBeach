"""Service turning the claims from an identity provider into a NearBeach user"""

from django.contrib.auth import get_user_model
from django.db import transaction
from django_otp.plugins.otp_email.models import EmailDevice
from django_otp.plugins.otp_totp.models import TOTPDevice

from NearBeach.models.authentication.oidc_provider import OidcIdentity, OidcProvider
from NearBeach.models.user import UserGroup
from NearBeach.services.OidcService import OidcError


class OidcUserService:
    """Class resolving, linking and creating users for a single OidcProvider"""

    def __init__(self, provider: OidcProvider) -> None:
        self.provider = provider
        self.user_model = get_user_model()

    def resolve(self, claims: dict):
        """Find (or make) the user for these claims, then check they are allowed in"""
        with transaction.atomic():
            user = self._user_from_identity(claims) or self._link_by_email(claims) or self._create_user(claims)

        if not user.is_active:
            raise OidcError("account_disabled")

        if not UserGroup.objects.filter(username=user, is_deleted=False).exists():
            raise OidcError("no_group")

        if not self.provider.trust_idp_mfa and self._has_two_factor_device(user):
            # NearBeach's own 2FA has no SSO step yet - fail closed rather than skip it
            raise OidcError("two_factor_required")

        return user

    def _user_from_identity(self, claims: dict):
        identity = OidcIdentity.objects.filter(
            provider=self.provider,
            subject=claims["sub"],
            is_deleted=False,
        ).select_related("user").first()
        return identity.user if identity else None

    @staticmethod
    def _verified_email(claims: dict) -> str:
        # Only an email the provider vouches for is safe to match on or store
        return claims.get("email", "") if claims.get("email_verified") is True else ""

    def _link_by_email(self, claims: dict):
        email = self._verified_email(claims)
        if not (self.provider.link_existing_by_email and email):
            return None

        matches = list(self.user_model.objects.filter(email__iexact=email)[:2])
        if len(matches) != 1:
            return None

        self._create_identity(matches[0], claims)
        return matches[0]

    def _create_user(self, claims: dict):
        provider = self.provider
        if not (provider.auto_create_users and provider.default_group and provider.default_permission_set):
            raise OidcError("no_account")

        user = self.user_model(
            username=self._unique_username(claims),
            email=self._verified_email(claims),
            first_name=claims.get("given_name", "")[:150],
            last_name=claims.get("family_name", "")[:150],
        )
        user.set_unusable_password()
        user.save()

        UserGroup.objects.create(
            username=user,
            group=provider.default_group,
            permission_set=provider.default_permission_set,
            change_user=user,
            creation_user=user,
        )
        self._create_identity(user, claims)
        return user

    def _create_identity(self, user, claims: dict) -> None:
        OidcIdentity.objects.create(
            user=user,
            provider=self.provider,
            subject=claims["sub"],
            change_user=user,
            creation_user=user,
        )

    def _unique_username(self, claims: dict) -> str:
        base = (claims.get("preferred_username") or claims.get("email") or claims["sub"])[:140]
        username, counter = base, 1
        while self.user_model.objects.filter(username__iexact=username).exists():
            counter += 1
            username = f"{base}-{counter}"
        return username

    @staticmethod
    def _has_two_factor_device(user) -> bool:
        return (
            TOTPDevice.objects.filter(user=user, confirmed=True).exists()
            or EmailDevice.objects.filter(user=user, confirmed=True).exists()
        )
