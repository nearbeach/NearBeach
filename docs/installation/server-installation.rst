.. _server-installation:

================================
Ubuntu 18.04 Server Installation
================================

--------------------
Minimum requirements
--------------------

^^^^^^^^
Hardware
^^^^^^^^

* 1GB RAM
* 1+ Core CPU (for small user base)
* 5+ GB Space (more for uploading documents)

^^^^^^^^
Software
^^^^^^^^

* Ubuntu 18.04
* Python 3.6+
* Django 2.1+
* Nginx
* Gunicorn
* MySQL

The following instructions will allow you to install Ubuntu 18.04 on your server.
These are just the quick steps and do not go into detail. If you wish to go into
more detail please visit the Ubuntu help site -
 `https://help.ubuntu.com/lts/serverguide/ <https://help.ubuntu.com/lts/serverguide/>`_

--------------------
Installation Process
--------------------

.. toctree::
  :maxdepth: 1
  :caption: Section 1 - Installation of Server
  :name: sec-installation-of-server

  sub_instructions/installation_of_server


.. toctree::
  :maxdepth: 1
  :caption: Section 2 - Installation of a Django and the setup of Gunicorn
  :name: sec-installation-of-django

  sub_instructions/installation_of_django

.. toctree::
  :maxdepth: 1
  :caption: Section 3 - Setup of Database
  :name: sec-installation-of-database

  sub_instructions/installation_of_mysql_server

.. toctree::
  :maxdepth: 1
  :caption: Section 4 - Installation of NearBeach
  :name: sec-installation-of-nearbeach

  sub_instructions/installation_of_nearbeach

.. toctree::
  :maxdepth: 1
  :caption: Optional steps
  :name: sec-installation-of-optional-steps

  sub_instructions/installation_of_optional_steps


.. toctree::
  :maxdepth: 1
  :caption: Optional steps
  :name: sec-optional-steps

  sub_instructions/trouble_shooting_issues
