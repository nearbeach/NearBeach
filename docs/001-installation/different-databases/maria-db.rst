.. _maria-db:

===========
Use MariaDb
===========

You can use NearBeach with MariaDB. You can easily run MariaDB within the same docker-compose file, or alternatively you can run it separately (external).

-----------------
External Database
-----------------

.. note::

    We recommend using an external database like AWS RDS, etc. So you can scale and backup externally to the docker container.

Below is the sample code for using MariaDB/MySQL. Please note we do not have any of the docker database setup, as this is not required for externally run databases.

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

.. note::

    This will run the database within the docker environment.

.. code-block:: bash

    version: '3'

    services:
       db:
           image: mariadb:10.11
           container_name: nearbeach-db
           ports:
           - 3306:3306
           environment:
           - MARIADB_DATABASE=<<Please fill>>
           - MARIADB_USER=<<Please fill>>
           - MARIADB_PASSWORD=<<Please fill>>
           - MARIADB_ROOT_PASSWORD=<<Please fill>>
           volumes:
           - ./init:/docker-entrypoint-initdb.d
       nearbeach:
           image: robotichead/nearbeach:latest
           container_name: nearbeach
           environment:
    ...

The above code would be used in your docker-compose file.

