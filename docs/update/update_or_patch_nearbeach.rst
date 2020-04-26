.. _update_or_patch_nearbeach:

==============================
Updating or Patching NearBeach
==============================

NearBeach and it's framework Django will need frequent updating/patching. (talk about security)


===============================
Updating Django (Web Framework)
===============================

It is recommended to install NearBeach on a Long Term Support (LTS) version of Django.
Security fixes/patches are applied for a longer period of time, helping keep your server secure.

NearBeach currently supports the following Django versions;

- Django Version 2.2 LTS
- Django Version 3.0

More information about upgrading Django can be found `found in the Django Documentation <https://docs.djangoproject.com/en/3.0/howto/upgrade-version/>`_

==================
Updating NearBeach
==================

NearBeach will be using the Semantic Versioning system. Version numbers will be
laid out as follows; major.minor.patch

1. MAJOR version changes means a new NearBeach. The changes are extensive that
  a new number for NearBeach is required.
2. MINOR version changes means new functionality in NearBeach. This could require
    - Database migrations
    - Static file migrations
3. PATCH versions mean very small changes. Usually this is to fix a bug or
  include a static file that was missing.


======
Method
======

1. Use ssh to connect with your web server

2. Use cd to navigate to your project directory

3. Activate your virtual environment for your web server

  .. code-block:: bash

    source <<virtualenv_location>>/bin/activate

4. Update NearBeach using PIP

  .. code-block:: bash

    pip install --upgrade NearBeach


  If you require a certain version of NearBeach, use the following code as an
  example

  .. code-block:: bash

    pip install NearBeach==0.26.0

5. Once NearBeach has been updated, you will still need to;
    - Apply any database Migrations
    - Collect any static files

6. Use the following code to apply any migrations

  .. code-block:: bash

    python3 ./manage.py migrate

7. Use the following code to collect any static files

  .. code-block:: bash

    python3 ./manage.py collectstatic

8. Refresh gunicorn to enforce the new version

  .. code-block:: bash

    sudo service gunicorn refresh


Your new version of NearBeach should be ready.
