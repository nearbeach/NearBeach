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

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Section 1 - Installation of Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :ref:`Installation of Server <sub_instructions/installation_of_server>`

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Section 2 - Installation of a Django and the setup of Gunicorn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :ref:`sub_instructions/installation_of_django`

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Section 3 - Setup of Database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :ref:`sub_instructions/installation_of_mysql_server`

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Section 4 - Installation of NearBeach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :ref:`sub_instructions/installation_of_nearbeach`

^^^^^^^^^^^^^^
Optional Steps
^^^^^^^^^^^^^^

Installation of Logs in NearBeach

Installation of NearBeach API

Connect Mapbox

Connect Google Maps

-----------------------
Trouble Shooting Issues
-----------------------

PDF Rendering gives 500 error
