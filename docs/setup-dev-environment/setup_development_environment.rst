.. _setup_development_environment:

=============================
Setup Development Environment
=============================

  .. attention:: If you would like any help setting up these environments, why not join our .. _a discord: https://discord.gg/64uhRztS6n


These instructions will help you install a development environment. Setup is
slightly different to a production environment.

It is recommended to install NearBeach on a Long Term Support (LTS) version of Django.
Security fixes/patches are applied for a longer period of time, helping keep your server secure.

NearBeach currently supports the following Django versions;

- Django Version 3.1+

More information about upgrading Django can be found `found in the Django Documentation <https://docs.djangoproject.com/en/3.0/howto/upgrade-version/>`_

.. note::
  The following instructions are for Ubuntu 18.04. If you are using a different operating system, modify the instructions to suit that operating system.

-----------------------
Download Git Repository
-----------------------

#. In a terminal, navigate to your project development folder

  .. code-block:: bash

    cd /<<project-dev-folder>>

#. Use Git to download NearBeach source code

  .. code-block:: bash

    git clone https://github.com/robotichead/NearBeach

#. First update and upgrade the system so you are working with the latest packages;

  .. code-block:: bash

    sudo apt-get update && sudo apt-get upgrade -y


#. Install the required system libraries for Django and NearBeach to working

  .. code-block:: bash

    sudo apt install python3-dev curl build-essential python3-setuptools shared-mime-info libjpeg-dev zlib1g-dev


#. Install pip

  .. code-block:: bash

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    sudo python3 get-pip.py


#. After installing the required packages, you will need to update pip

  .. code-block:: bash

    sudo pip3 install --upgrade pip


#. Once pip is upgraded, you will need to create a virtual environment

  .. code-block:: bash

    sudo pip3 install virtualenv

#. Create your own virtual environment for python

  .. code-block:: bash

    virtualenv <<project_environment>>

  This will create a directory called "<<project_environment>>", this will store NearBeach's libraries for python

#. Activate the virtual environment using the following command

  .. code-block:: bash

    source ./<<project_environment>>/bin/activate

  You terminal prompt will change to indicate that it is working in the virtual environment now. It should look like the following

  .. code-block:: bash

    (<<project_environment>>)user@computer:

#. Install Django

  .. code-block:: bash

    pip install django


#. Create your project

  .. code-block:: bash

  djangoadmin startproject <<django_project>>

  .. note:: Please do NOT call the <<django_project>> NearBeach, or any variation of it.


#. Adjust the project's settings to allow debugging and accept ALL allowed hosts

  .. code-block:: bash

    nano ./<<django_project>>/<<django_project>>/settings.py


#. Change the following lines to reflect the following

  ..image:: images/django-installation-001.png

  This will allow us to test the web server.

  Save the settings file and exit

14. Run the following command to see if Django is running

  .. code-block:: bash

    python3 ./manage.py runserver

  If the server runs fine - then we can proceed.

15. Symbolic link in NearBeach's source code

  .. code-block:: bash

    ln -s /<<project-dev-folder>>/NearBeach/NearBeach /<<project-dev-folder>>/<<django_project>>

  This code will place the core NearBeach code into the Django's project directory.

16. Navigate to your project's folder

  .. code-block:: bash

    $ cd <<django_project_location>>

17. Install all required python files using pip

  .. code-block:: bash

    pip3 install -r ./NearBeach/requirements.txt

18. Edit the project's settings.py to include NearBeach

  .. code-block:: bash

    $ nano ./<<django_project>>/<<django_project>/settings.py

19. Add the following line to the top of "INSTALLED_APPS" section

  .. code-block:: bash

    'NearBeach.apps.NearBeachConfig',

  Now save the document

20. Email - optional however required for resetting passwords

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

21. Private Documents

  .. code-block:: bash

    nano ./<<project name>>/settings.py

  Add the following lines of code into the settings.py

  .. code-block:: bash

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

  .. code-block:: bash

    STATIC_URL = '/static/'
    STATIC_ROOT= os.path.join(BASE_DIR,'static/')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR,'media/')

22. Edit the project's URL.py to include NearBeach

  .. code-block:: bash

    nano ./<<django_project>>/url.py

  Please make sure that the following import in included at the top of the file

  .. code-block:: bash

    from django.urls import path, include

  Either of the following can be entered into the "urlpatterns" section

  .. code-block:: bash

    path('', include('NearBeach.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('select2/', include('django_select2.urls')),

23. Create Database/Migrations

  The database will need to be setup. Please note by default Django uses sqlite3, however it is possible to setup NearBeach to use a mysql database.

  .. code-block:: bash

    python ./manage.py migrate
    python ./manage.py migrate NearBeach

  If you have setup NearBeach with an SQLite database, you will need to change it's permissions so nginx can access it

  ..  code-block:: bash

    sudo chmod 7777 ./db.sqlite

24. Create superuser
  A superuser will need to be created. This superuser will be able to enter the ADMIN site of Django, which from there will be able to do administration items.

  .. code-block:: bash

    python ./manage.py createsuperuser

  Enter in the correct details for the superuser

25. Collect the static

  The website uses static images, javascript, and CSS. You will need to collect this data to the static folder (set in the settings.py). Please run the following command

  .. code-block:: bash

    python ./manage.py collectstatic

26. Create the private media folder

  .. code-block:: bash

    $ mkdir ./private_media/

The NearBeach development environment should now be setup on your local.

.. note:: The first user to log in will automatically get administration permissions. It is recommended to get the system admin to log in first before importing any user data from other sources. This also allows the admin to setup groups and permissions.
