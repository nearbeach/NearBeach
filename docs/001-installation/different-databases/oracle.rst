.. _postgresql:

=============
Use Oracle DB
=============

You can use NearBeach with Oracle.

-----------------
External Database
-----------------

.. note::

    We recommend using an external database like AWS RDS, etc. So you can scale and backup externally to the docker container.
You will need to fill out the following fields. These fields should match how you would log into that database.

Below is the sample code for using Oracle DB. Please note we do not have any of the docker database setup, as this is not required for externally run databases.

.. code-block:: bash

    version: '3'

    services:
        nearbeach:
            image: robotichead/nearbeach:latest
            container_name: nearbeach
            environment:
            ...
            - DB_DATABASE=<<Please fill>>
            - DB_USER=<<Please fill>>
            - DB_PASSWORD=<<Please fill>>
            - DB_HOST=<<please fill>>
            - DB_ENGINE=oracle
            - DB_PORT=<<please fill>>
            ...

You will need to fill out the following fields. These fields should match how you would log into that database.

- DB_DATABASE=<<Please fill>>
- DB_USER=<<Please fill>>
- DB_PASSWORD=<<Please fill>>
- DB_HOST=<<please fill>>
- DB_ENGINE=oracle
- DB_PORT=<<please fill>>

