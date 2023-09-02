.. _postgresql:

==============
Use PostgreSQL
==============

You can use NearBeach with PostgreSQL. You can easily run PostgreSQL within the same docker-compose file, or alternatively you can run it separately (external).

-----------------
External Database
-----------------

.. note::

    We recommend using an external database like AWS RDS, etc. So you can scale and backup externally to the docker container.
You will need to fill out the following fields. These fields should match how you would log into that database.

Below is the sample code for using PostgreSQL. Please note we do not have any of the docker database setup, as this is not required for externally run databases.

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
            - DB_ENGINE=postgresql
            - DB_PORT=<<please fill>>
            ...

You will need to fill out the following fields. These fields should match how you would log into that database.

- DB_DATABASE=<<Please fill>>
- DB_USER=<<Please fill>>
- DB_PASSWORD=<<Please fill>>
- DB_HOST=<<please fill>>
- DB_ENGINE=postgresql
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
           image: postgres:latest
           container_name: nearbeach-db
           ports:
           - 5432:5432
           environment:
           - POSTGRES_DB=<<Please fill>>
           - POSTGRES_USER=<<Please fill>>
           - POSTGRES_PASSWORD=<<Please fill>>
           volumes:
           - ./db-data/:/var/lib/postgresql/data/
           - ./init:/docker-entrypoint-initdb.d
       nearbeach:
           image: robotichead/nearbeach:latest
           container_name: nearbeach
           environment:
    ...

The above code would be used in your docker-compose file.

