.. _single-sign-on:

Single Sign-On (OpenID Connect)
###############################

NearBeach can let people sign in through an external identity provider that speaks OpenID Connect (OIDC) - for
example Keycloak, Microsoft Entra ID, Google or Okta. Each provider you configure adds a "Sign in with ..." button to
the login page. Password login keeps working alongside it.

Providers are set up in the Django admin site (``/admin/``), under **OIDC Providers**. Only superusers can do this.


Before You Start
================

In your identity provider, register NearBeach as a client application and note down its client ID and secret.

* **Redirect URI** - ``https://<your NearBeach host>/api/v1/authentication/oidc/<slug>/callback/``, where ``<slug>`` is
  the slug you give the provider in NearBeach (e.g. ``keycloak``). It must match exactly, including ``https``.
* **Flow** - Authorization Code. NearBeach always uses PKCE.
* **Scopes** - ``openid``, ``email`` and ``profile``.


Adding a Provider
=================

1. Log into the Django admin site and choose **OIDC Providers** > **Add**

2. Fill in the fields:

   ========================== ====================================================================================
   Name                       Shown on the login button
   Slug                       Used in the URLs - must match the redirect URI registered with the provider
   Issuer url                 The provider's issuer. NearBeach reads ``<issuer>/.well-known/openid-configuration``
   Client id / Client secret  From the provider. Leave the secret blank for a public (PKCE only) client
   Scopes                     Defaults to ``openid email profile``
   Is enabled                 Untick to hide the button without deleting the provider
   ========================== ====================================================================================

3. Decide who is allowed in (see below), then save


Who Is Allowed In
=================

NearBeach never creates accounts at sign in. An administrator creates each user first (**Administration** >
**Users**) and puts them in a group. Anyone else who signs in through the provider is turned away.

A person is matched to their NearBeach user in this order:

1. **Already linked** - they have signed in with this provider before. Matching uses the provider's stable ``sub``
   identifier, never the email address.

2. **Link existing user by email** - if ticked, a first-time sign in is linked to the NearBeach user with the same
   email address. This only happens when the provider says the email is **verified**, and only when exactly one
   NearBeach user has that email. Once linked, the email is no longer used - the ``sub`` is.

If neither applies, the person is sent back to the login page with a message saying they have no account, and nothing
is created. An administrator can also link a person by hand: in the Django admin, add an **OIDC Identity** with the
user, the provider, and the provider's ``sub`` for that person.

The user must be active and belong to at least one group, otherwise they are turned away with a message saying so.

To onboard someone: create their NearBeach user with the same email address they use at the provider, add them to a
group, and ask them to use the "Sign in with ..." button.


Two-Factor Authentication
=========================

* If **Trust idp mfa** is ticked, NearBeach does not ask for its own two-factor code - the provider is responsible for
  multi-factor authentication.
* If it is not ticked, a user who has set up two-factor authentication in NearBeach **cannot** sign in through the
  provider yet, and is asked to use their password instead. Tick the box once your provider enforces MFA.


Security Notes
==============

* The client secret is stored in the NearBeach database. Restrict access to the Django admin site accordingly.
* Rotate the secret in the provider and NearBeach together if it is ever exposed.
* Users created by single sign-on cannot use "Forgotten Password" until they set a password.


Keycloak Example
================

1. In Keycloak, open your realm > **Clients** > **Create client**

2. Client type **OpenID Connect**, client ID ``nearbeach``

3. Turn **Client authentication** on and keep **Standard flow** ticked

4. Set **Valid redirect URIs** to ``https://<your NearBeach host>/api/v1/authentication/oidc/keycloak/callback/``

5. On the **Credentials** tab, copy the client secret

6. In NearBeach, add a provider with:

   * Slug ``keycloak``
   * Issuer url ``https://<keycloak host>/realms/<realm>``
   * The client ID and secret from above

7. Visit the login page - a "Sign in with Keycloak" button now appears


Single Sign-On Troubleshooting
==============================

The login page shows a message when something goes wrong. The server log has the detail - search for
``OIDC login for <slug> failed``.

* *No NearBeach account exists* - the person has no linked user. Create the user first, with the same email address
  they use at the provider (and tick **Link existing by email**), or add an **OIDC Identity** by hand.
* *Not been added to a group* - the user has no group. Add them in **Administration** > **Users**.
* *Could not be reached* - NearBeach cannot read the provider's discovery document. Check the issuer url, and that it
  matches the ``issuer`` the provider reports exactly.
* *Single sign-on failed* - usually a wrong client secret, a redirect URI that does not match, or a clock that is more
  than a minute out of step with the provider.
