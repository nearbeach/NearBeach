.. _basic_docker_installation:

=========================
Basic Docker Installation
=========================

Please copy the example code into a text editor of your choice

.. code-block:: Docker

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
        image: robotichead/nearbeach:development-0.30.0
        container_name: nearbeach
        environment:
        - SECRET_KEY=<<Please fill>>
        - SMTP_EMAIL_HOST=<<Please fill>>
        - SMTP_EMAIL_PORT=<<Please fill>>
        - SMTP_EMAIL_HOST_USER=<<Please fill>>
        - SMTP_EMAIL_HOST_PASSWORD=<<Please fill>>
        - MYSQL_DATABASE=<<Please fill>>
        - MYSQL_USER=<<Please fill>>
        - MYSQL_PASSWORD=<<Please fill>>
        - MYSQL_HOST=nearbeach-db
        - ADMIN_USERNAME=<<Please fill>>
        - ADMIN_EMAIL=<<Please fill>>
        - CSRF_TRUSTED_URLS=<<https://yourdomain.com.au>>
        - AZURE_STORAGE_CONNECTION_STRING=<<Please fill>>
        - AZURE_STORAGE_CONTAINER_NAME=<<Please fill>>
        volumes:
        - .:/ceansuite
        ports:
        - 8000:8000
        - 2525:2525
        command: >
            sh -c "python manage.py wait_for_database &&
                ls -al &&
                python manage.py migrate &&
                python manage.py initadmin &&
                python manage.py runserver 0.0.0.0:8000"
        restart: unless-stopped
        depends_on:
        - db


Please fill out the appropriate details for the following fields;
- SMTP_EMAIL_HOST
- SMTP_EMAIL_PORT
- SMTP_EMAIL_HOST_USER
- SMTP_EMAIL_HOST_PASSWORD
- ADMIN_USERNAME
- ADMIN_EMAIL 


Please fill out the appropriate details for the following fields. Please note that the following fields will require the exact same values.
- MYSQL_DATABASE / MARIADB_DATABASE
- MYSQL_USER / MARIADB_USER
- MYSQL_PASSWORD / MARIADB_PASSWORD
- MARIADB_ROOT_PASSWORD


Fill out the following field with the domain you are going to use for your NearBeach Instance;
- CSRF_TRUSTED_URLS=https://yourdomain.com.au
Please note the https - it is recommended to use https when using NearBeach.


Use your Azure Blob storage to store uploaded files from NearBeach. If you don't require Azure Blob storage, please delete these two lines.


Save the file in an appropriate location called `docker-compose.yml``


Using a terminal, change directory to the location that you stored the docker-compose file. Run the following command: `docker-compose up -D`