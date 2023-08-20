.. _installation_of_nearbeach:

=========================
Installation of NearBeach
=========================

The following instructions will inform you how to setup NearBeach and get it running on your Web Server.

1. You will need to be in your virtual environment

  .. code-block:: bash

    source <<virtualenv_location>>/bin/activate

2. Navigate to your project's folder

  .. code-block:: bash

    $ cd <<django_project_location>>

3. Install NearBeach through PIP. This will install NearBeach as well as all the required libraries utilised by NearBeach.

  .. code-block:: bash

    pip install NearBeach

4. Edit the project's settings.py to include NearBeach

  .. code-block:: bash

    $ nano ./<<project name>>/settings.py

5. Add the following line to the "INSTALLED_APPS" section

  .. code-block:: bash

    'NearBeach.apps.NearBeachConfig',

  Now save the document and add the following two lines to the "context_processors" under "TEMPLATES".

  .. code-block:: bash

    'NearBeach.context_processors.django_version',
    'NearBeach.context_processors.nearbeach_version',

  These two lines will render the version of both Django and NearBeach inside the templates.

6. Enabling reCAPTCHA (optional). Register an account at [Google reCAPTCHA](https://www.google.com/recaptcha/intro/invisible.html).

  .. code-block:: bash

    $ nano ./<<project name>>/settings.py

  The following variables will need to be placed into your settings.py.

  .. code-block:: bash

    RECAPTCHA_PUBLIC_KEY = 'Your public key'
    RECAPTCHA_PRIVATE_KEY = 'Your private key'


7. Security - Add the following lines of code into the settings.py
  
  .. code-block:: bash
  
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_HTTPONLY = True


8. Email - optional however required for resetting passwords

  .. code-block:: bash

    $ nano ./<<project name>>/settings.py

  Add the following lines of code into the settings.py

  .. code-block:: bash

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = '<< your email host >>'
    EMAIL_PORT = 25
    EMAIL_HOST_USER = '<< your username >>'
    EMAIL_HOST_PASSWORD = '<< your password >>'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

9. Private Documents

  .. code-block:: bash

    nano ./<<project name>>/settings.py

  Add the following lines of code into the settings.py

  .. code-block:: bash

    PRIVATE_MEDIA_URL = '/private/' #Can change
    if DEBUG:
        # dev
        import os

        PRIVATE_MEDIA_ROOT = os.path.abspath(os.path.dirname(__file__))
        PRIVATE_MEDIA_SERVER = 'DefaultServer'
    else:
        # prod
        PRIVATE_MEDIA_ROOT = '<< folder containing private folder >>'
        PRIVATE_MEDIA_SERVER = 'ApacheXSendfileServer'


  .. note::

    Please note: The PRIVATE_MEDIA_ROOT variable will only contain the folder that contains the Private
    folder. The system will automatically append the 'private' variable onto the end of PRIVATE_MEDIA_ROOT.

  The following redundant code will need to be used at the moment.

  .. code-block:: bash

    STATIC_URL = '/static/'
    STATIC_ROOT= os.path.join(BASE_DIR,'static/')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR,'media/')

10. Edit the project's URL.py to include NearBeach

  .. code-block:: bash

    nano ./<<project name>>/url.py

  Please make sure that the following import in included at the top of the file

  .. code-block:: bash

    from django.urls import path, include

  Either of the following can be entered into the "urlpatterns" section

  .. code-block:: bash

    path('', include('NearBeach.urls')),

11. Create Database/Migrations

  The database will need to be setup. Please note by default Django uses sqlite3, however it is possible to setup NearBeach to use a mysql database.

  .. code-block:: bash

    python ./manage.py migrate
    python ./manage.py migrate NearBeach

  If you have setup NearBeach with an SQLite database, you will need to change it's permissions so nginx can access it

  ..  code-block:: bash

    sudo chmod 755 ./db.sqlite

12. Create superuser
  A superuser will need to be created. This superuser will be able to enter the ADMIN site of Django, which from there will be able to do administration items.

  .. code-block:: bash

    python ./manage.py createsuperuser

  Enter in the correct details for the superuser

13. Collect the static

  The website uses static images, javascript, and CSS. You will need to collect this data to the static folder (set in the settings.py). Please run the following command

  .. code-block:: bash

    python ./manage.py collectstatic


14. Create the private media folder

  .. code-block:: bash

    $ mkdir ./private_media/

15. Assign write permissions to the ./media/ and ./private_media/ folder

  .. code-block:: bash

    $ sudo chmod -R 755 ./media
    $ sudo chmod -R 755 ./private_media

  Restart gunicorn

  .. code-block:: bash

    $ sudo service gunicorn restart

NearBeach should now be setup for you on your server. Navigate to your server's Domain Name or IP address and you should see the login screen. Please note it is recommended to have HTTPS enabled, we recommend Lets Encrypt. Please see https://letsencrypt.org/ and follow the prompts to get Cert Bot installed.

.. note:: The first user to log in will automatically get administration permissions. It is recommended to get the system admin to log in first before importing any user data from other sources. This also allows the admin to setup groups and permissions.
