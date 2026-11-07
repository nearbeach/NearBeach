.. _oauth2-api:

OAuth2 Bearer Tokens for the API
################################

NearBeach can issue OAuth2 access tokens, so other systems can call the API with an ``Authorization: Bearer <token>``
header instead of a username and password. Two ways of getting a token are supported:

* **Client credentials** - for server-to-server integrations (reporting, CI, scripts). The integration is its own
  "person", a *service user* you set up.
* **Authorization code with PKCE** - for apps acting on behalf of a person, who signs in to NearBeach and approves the
  access. Returns a refresh token too.

Existing ``Token`` (Knox) and session authentication keep working as before. Basic authentication still works too, but
not for a user who has set up two-factor authentication - a password alone would get around it. Those users sign in
through the login page, or use a token.


What a Token Can Do
===================

A token acts as a user, so it can only ever do what that user's groups and permission sets allow. On top of that, each
token carries scopes that can narrow it further:

======= =====================================================================================
read    ``GET`` and ``HEAD`` requests
write   ``POST``, ``PATCH`` and ``DELETE`` requests (``write`` also allows reading)
======= =====================================================================================

Scopes never grant extra rights. A ``write`` token for a user with read-only permissions still cannot write.

Access tokens last one hour. Refresh tokens last 14 days and are replaced every time they are used.


Setting Up an Integration (Client Credentials)
==============================================

1. **Create a service user.** In **Administration** > **Users**, create a user for the integration (e.g.
   ``reporting-bot``), and add it to the groups it needs with a suitable permission set. Give it the least access that
   does the job. Do not reuse a person's account.

2. **Register the application.** In the Django admin site (``/admin/``), under **Django OAuth Toolkit** >
   **Applications** > **Add**:

   ============================ ================================================================================
   User                         The service user from step 1. **Required** - a token for an application with no
                                user is rejected
   Client type                  Confidential
   Authorization grant type     Client credentials
   Name                         Anything that tells you what it is for
   ============================ ================================================================================

3. **Copy the client secret before saving.** It is hashed when saved and can never be shown again. If it is lost,
   edit the application and set a new one.

4. **Ask for a token:**

   .. code-block:: bash

      curl -X POST https://<your NearBeach host>/o/token/ \
        -d grant_type=client_credentials \
        -d client_id=<client id> \
        -d client_secret=<client secret> \
        -d scope=read

   The response contains ``access_token``. Request ``scope="read write"`` for an integration that makes changes.

5. **Call the API:**

   .. code-block:: bash

      curl https://<your NearBeach host>/api/v1/project/ \
        -H "Authorization: Bearer <access token>"

Ask for a new token when the old one expires - there is no refresh token for client credentials.


Apps Acting for a Person (Authorization Code)
=============================================

Register the application as above but choose **Authorization code** as the grant type, list the exact **Redirect
uris** (``https`` only), and set **Client type** to *Public* for apps that cannot keep a secret (mobile and
single-page apps).

* PKCE is **required**. The app sends a ``code_challenge`` (method ``S256``) when it starts, and the matching
  ``code_verifier`` when it swaps the code for a token.
* The person is sent to ``/o/authorize/``. If they are not signed in they are sent to the NearBeach login page first
  (which includes single sign-on), then asked to approve the access.
* The token acts as that person.

Endpoints
---------

======================= =========================================
``/o/authorize/``       Where a person approves access
``/o/token/``           Get a token, or swap a refresh token
``/o/revoke_token/``    Cancel an access or refresh token
======================= =========================================

The token endpoint is rate limited in the same way as the login page. Too many attempts get a ``429`` response.


Revoking Access
===============

* **One token** - the client calls ``/o/revoke_token/``, or delete it under **Access tokens** in the Django admin.
* **A whole integration** - delete the application, or disable its service user. Existing tokens stop working
  straight away.
* **A user who resets their password** - all of their Knox and OAuth2 tokens are cancelled, including those of an
  application they are the service user for. Integrations using them need new tokens.


Troubleshooting
===============

* ``401 invalid_client`` - wrong client ID or secret.
* ``400 invalid_scope`` - only ``read`` and ``write`` exist.
* ``401``/``403`` on an API call - the token has expired or been revoked; the application has no service user; or the
  service user is disabled.
* ``403 ... does not have the scope`` - the token was issued with ``read`` only, but the request changes data.
* ``403`` with a valid token - the service user's groups do not allow that action.
