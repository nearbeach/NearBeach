.. _installation_of_optional_steps:

==============
Optional Steps
==============

--------------
Connect Mapbox
--------------

The following instructions will help you install the Mapbox API. This API will allow you to;

1. Obtain Coordinates of campus locations

2. Display a map of the coordinates

3. Navigate to your project's folder

  .. code-block:: bash

    $ cd /var/www/<project_name>

4. Edit the project's settings.py to include Mapbox

  .. code-block:: bash

    $ nano ./<<project name>>/settings.py


5. Add the following line to the "INSTALLED_APPS" section

  .. code-block:: bash

    MAPBOX_API_TOKEN = '<<MAPBOX_API_TOKEN>>'

NearBeach will automatically find the Mapbox token and start displaying the maps. If the maps are not displaying please check that you are using the correct API Token

---------------------------------
Installation of Logs in NearBeach
---------------------------------

-------------------
Connect Google Maps
-------------------
