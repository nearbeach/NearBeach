from django.contrib import admin

from NearBeach.models.authentication.oidc_provider import OidcIdentity, OidcProvider


@admin.register(OidcProvider)
class OidcProviderAdmin(admin.ModelAdmin):
    """Admin page to configure the single sign-on providers"""

    list_display = ("name", "slug", "issuer_url", "is_enabled")
    prepopulated_fields = {"slug": ("name",)}
    exclude = ("is_deleted",)

    def save_model(self, request, obj, form, change):
        obj.change_user = request.user
        if not change:
            obj.creation_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(OidcIdentity)
class OidcIdentityAdmin(admin.ModelAdmin):
    """Read-mostly view of which users are linked to which provider"""

    list_display = ("user", "provider", "subject")
    exclude = ("is_deleted",)
