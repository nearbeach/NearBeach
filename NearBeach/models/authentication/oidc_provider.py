"""Module providing the OpenID Connect (SSO) tables for NearBeach"""

from django.conf import settings
from django.db import models

from NearBeach.models.abstraction.common_abstractions import CommonInfo
from NearBeach.models.permission.group import Group
from NearBeach.models.permission.permission_set import PermissionSet


class OidcProvider(CommonInfo):
    """Class containing the configuration of an OpenID Connect identity provider (Keycloak, Entra, Google, etc.)"""

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=50,
        help_text="Shown on the login button",
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )
    issuer_url = models.URLField(
        help_text="The provider's issuer URL. Its discovery document lives at <issuer>/.well-known/openid-configuration",
    )
    client_id = models.CharField(
        max_length=255,
    )
    client_secret = models.CharField(
        max_length=512,
        blank=True,
        default="",
        help_text="Leave blank for public clients (PKCE only)",
    )
    scopes = models.CharField(
        max_length=255,
        default="openid email profile",
    )
    is_enabled = models.BooleanField(
        default=True,
    )
    auto_create_users = models.BooleanField(
        default=False,
        help_text="Create a NearBeach user the first time someone signs in. Requires a default group",
    )
    link_existing_by_email = models.BooleanField(
        default=False,
        help_text="Link a first-time sign in to the NearBeach user with the same email. Only used when the "
                  "provider reports the email as verified",
    )
    trust_idp_mfa = models.BooleanField(
        default=False,
        help_text="Skip NearBeach two-factor authentication for users signing in through this provider",
    )
    default_group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="Group given to users created by this provider",
    )
    default_permission_set = models.ForeignKey(
        PermissionSet,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="Permission set given to users created by this provider",
    )

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        """Meta definitions for OidcProvider"""

        verbose_name_plural = "OIDC Providers"


class OidcIdentity(CommonInfo):
    """Class linking a NearBeach user to their account at an identity provider"""

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="oidc_identities",
    )
    provider = models.ForeignKey(
        OidcProvider,
        on_delete=models.CASCADE,
    )
    subject = models.CharField(
        max_length=255,
        help_text="The provider's stable identifier for the user (the `sub` claim)",
    )

    def __str__(self) -> str:
        return f"{self.provider} - {self.subject}"

    class Meta:
        """Meta definitions for OidcIdentity"""

        verbose_name_plural = "OIDC Identities"
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "subject"],
                name="unique_oidc_provider_subject",
            ),
        ]
