====================
Welcome to NearBeach
====================

.. image:: https://img.shields.io/github/license/robotichead/NearBeach
.. image:: https://img.shields.io/pypi/v/NearBeach
.. image:: https://img.shields.io/circleci/build/github/robotichead/NearBeach/master
.. image:: https://img.shields.io/codeclimate/maintainability/robotichead/NearBeach


NearBeach is an Open Source Project Management system built on the Django
framework. `NearBeach.org <https://nearbeach.org/>`_

.. note:: NearBeach is licensed under the MIT license

-----------------------
NearBeach documentation
-----------------------
NearBeach's documentation is broken down into the following sections;

* Installation of a new Server
* Installation of a new NearBeach instance
* Administration tasks and first time setup
* Basic User instructions

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

  installation/installation_of_server


.. toctree::
  :maxdepth: 1
  :caption: Section 2 - Installation of a Django and the setup of Gunicorn
  :name: sec-installation-of-django

  installation/installation_of_django


.. toctree::
  :maxdepth: 1
  :caption: Section 3 - Setup of Database
  :name: sec-installation-of-database

  installation/installation_of_mysql_server


.. toctree::
  :maxdepth: 1
  :caption: Section 4 - Installation of NearBeach
  :name: sec-installation-of-nearbeach

  installation/installation_of_nearbeach


.. toctree::
  :maxdepth: 1
  :caption: Optional steps
  :name: sec-installation-of-optional-steps

  installation/installation_of_optional_steps


.. toctree::
  :maxdepth: 1
  :caption: Optional steps
  :name: sec-optional-steps

  installation/trouble_shooting_issues

  ------------------
  After Installation
  ------------------

.. toctree::
  :maxdepth: 1
  :caption: Administration tasks
  :name: sec-administration-tasks

  administration-tasks/first-time-setup
  administration-tasks/configuration

.. toctree::
  :maxdepth: 1
  :caption: Basic usage
  :name: sec-basic-usage

  basic-usage/nearbeach-flow
  basic-usage/opportunities
  basic-usage/quotes-and-invoices
  basic-usage/requirements-and-requirement-items
  basic-usage/projects
  basic-usage/tasks
  basic-usage/requests-for-change
