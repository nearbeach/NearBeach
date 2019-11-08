NearBeach Installation
======================

The following instructions will inform you how to setup NearBeach and get it running on your Web Server.

    You will need to be in your virtual environment
    source <<virtualenv_location>>/bin/activate
    Navigate to your project's folder
    $ cd <<django_project_location>>
    Install NearBeach through PIP. This will install NearBeach as well as all the required libraries utilised by NearBeach.
    pip install NearBeach
    Edit the project's settings.py to include NearBeach
    $ nano ./<<project name>>/settings.py
    Add the following line to the "INSTALLED_APPS" section
    'NearBeach.apps.NearBeachConfig',
    'django.contrib.humanize',
    'tinymce',
    'django_select2',


    Now save the document
    Enabling reCAPTCHA (optional). Register an account at [Google reCAPTCHA](https://www.google.com/recaptcha/intro/invisible.html).
    $ nano ./<<project name>>/settings.py
    The following variables will need to be placed into your settings.py.
    RECAPTCHA_PUBLIC_KEY = 'Your public key'
    RECAPTCHA_PRIVATE_KEY = 'Your private key'

    Security - Add the following lines of code into the settings.py
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_HTTPONLY = True

    Email - optional however required for resetting passwords

    $ nano ./<<project name>>/settings.py
    Add the following lines of code into the settings.py
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = '<< your email host >>'
    EMAIL_PORT = 25
    EMAIL_HOST_USER = '<< your username >>'
    EMAIL_HOST_PASSWORD = '<< your password >>'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

    Private Documents

    nano ./<<project name>>/settings.py

    Add the following lines of code into the settings.py

    PRIVATE_MEDIA_URL = '/private/' #Can change
    if DEBUG:
        # dev
        import os

        PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
        PRIVATE_MEDIA_ROOT = os.path.join(PROJECT_PATH, 'private')
        PRIVATE_MEDIA_SERVER = 'DefaultServer'
    else:
        # prod
        PRIVATE_MEDIA_ROOT = '<< private documents location >>'
        PRIVATE_MEDIA_SERVER = 'ApacheXSendfileServer'

    The following redundant code will need to be used at the moment.

    STATIC_URL = '/static/'
    STATIC_ROOT= os.path.join(BASE_DIR,'static/')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR,'media/')

    Edit the project's URL.py to include NearBeach

    nano ./<<project name>>/url.py

    Please make sure that the following import in included at the top of the file
    from django.urls import path, include

    Either of the following can be entered into the "urlpatterns" section

    path('', include('NearBeach.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('select2/', include('django_select2.urls')),

    Create Database/Migrations
    The database will need to be setup. Please note by default Django uses sqlite3, however it is possible to setup NearBeach to use a mysql database.

    python ./manage.py migrate
    python ./manage.py migrate NearBeach

    If you have setup NearBeach with an SQLite database, you will need to change it's permissions so nginx can access it
    sudo chmod 7777 ./db.sqlite

    Create superuser
    A superuser will need to be created. This superuser will be able to enter the ADMIN site of Django, which from there will be able to do administration items.

    python ./manage.py createsuperuser

    Enter in the correct details for the superuser


    Collect the static

    The website uses static images, javascript, and CSS. You will need to collect this data to the static folder (set in the settings.py). Please run the following command

    python ./manage.py collectstatic


    Create the private media folder
    $ mkdir ./private_media/

    Assign write permissions to the ./media/ and ./private_media/ folder
    $ sudo chmod -R 777 ./media
    $ sudo chmod -R 777 ./private_media
    Restart gunicorn
    $ sudo service gunicorn restart

NearBeach should now be setup for you on your server. Navigate to your server's Domain Name or IP address and you should see the login screen. Please note it is recommended to have HTTPS enabled, we recommend Lets Encrypt. Please see https://letsencrypt.org/ and follow the prompts to get Cert Bot installed.


Note - the first user to log in will automatically get administration permissions. It is recommended to get the system admin to log in first before importing any user data from other sources. This also allows the admin to setup groups and permissions.