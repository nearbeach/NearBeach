.. _maria-db:

===========
Use MariaDb
===========

You can use NearBeach with MariaDB

-----------------
External Database
-----------------

.. note::

    We recommend using an external database like RDS etc. So you can scale and backup externally to the docker container.

Below is the sample code for using MariaDB/MySQL

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
            - DB_ENGINE=mysql
            - DB_PORT=<<please fill>>
            ...

You will need to fill out the following fields. These fields should match how you would log into that database.

- DB_DATABASE=<<Please fill>>
- DB_USER=<<Please fill>>
- DB_PASSWORD=<<Please fill>>
- DB_HOST=<<please fill>>
- DB_ENGINE=mysql
- DB_PORT=<<please fill>>

---------------
Docker Database
---------------