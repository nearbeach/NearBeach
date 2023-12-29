.. _quick-install:

=========================
Quick Install with Docker
=========================

Copy the following code and paste it into a file called `docker-compose.yaml`

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
            - SECRET_KEY=<<Please fill>>
            - SMTP_EMAIL_HOST=<<Please fill>>
            - SMTP_EMAIL_PORT=<<Please fill>>
            - SMTP_EMAIL_HOST_USER=<<Please fill>>
            - SMTP_EMAIL_HOST_PASSWORD=<<Please fill>>
            - DB_DATABASE=<<Please fill>>
            - DB_USER=<<Please fill>>
            - DB_PASSWORD=<<Please fill>>
            - DB_HOST=nearbeach-db
            - DB_ENGINE=mysql
            - DB_PORT=3306
            - ADMIN_USERNAME=<<Please fill>>
            - ADMIN_EMAIL=<<Please fill>>
            - CSRF_TRUSTED_URLS=<<https://yourdomain.com.au>>
            - ALLOWED_HOSTS=localhost,127.0.0.1
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


#. Inside the docker-compose.yaml file, edit the SECRET_KEY. This will be a large string with symbols, letters and
numbers. You can use a generate like https://djecrety.ir/


#. Inside the docker-compose.yaml file, fill out the following fields appropriately. SMTP is used to send the reset
password functionality required to login for the first time.

    - SMTP_EMAIL_HOST
    - SMTP_EMAIL_PORT
    - SMTP_EMAIL_HOST_USER
    - SMTP_EMAIL_HOST_PASSWORD


#. The administration username/email will be used to log into NearBeach. This will need to be filled out appropriately
because changing

    - ADMIN_USERNAME
    - ADMIN_EMAIL


#. Inside the docker-compose.yaml file, there are two services. One will be for setting up the Database, and the other
service will setup NearBeach. You will need to fill out the database connection/details. Please note you will need the
same variable value for the following pairs;

    - DB_DATABASE / MARIADB_DATABASE
    - DB_USER / MARIADB_USER
    - DB_PASSWORD / MARIADB_PASSWORD
    - MARIADB_ROOT_PASSWORD

    MARIADB_ROOT_PASSWORD will not have a pair.


#. Fill out the CSRF_TRUSTED_URLS value. This will need to be the EXACT domain. Please view the examples below

    .. code-block:: bash

        CSRF_TRUSTED_URLS=https://demo.nearbeach.org

    If you would like to demo NearBeach, please fill out the following

    .. code-block:: bash

        CSRF_TRUSTED_URLS=http://localhost:8000,http://127.0.0.1:8000

#. Fill out the ALLOWED_HOSTS. This will be similar to the CSRF_TRUSTED, but without the http and port numbers.

    .. code-block:: bash

        - ALLOWED_HOST=demo.nearbeach.org


    Alternatively - if using localhost


    .. code-block:: bash

        - ALLOWED_HOSTS=localhost,127.0.0.1


#. Use your Azure Blob storage to store uploaded files from NearBeach. If you don't require Azure Blob storage, please
delete these two lines;

    .. code-block:: bash

        - AZURE_STORAGE_CONNECTION_STRING
        - AZURE_STORAGE_CONTAINER_NAME


#. Using a terminal, change directory to the location that you stored the docker-compose file. Run the following
command: `docker-compose up -d`. If you would like to specify a project name for your NearBeach instance. Run the
following command instead: `docker-compose up -d --project-name NearBeach`.


You are now up and running NearBeach in Docker. Visiting the URL you set in the `CSRF_TRUSTED_URLS` in your browser will
take you to NearBeach. For first time logins, you will need to reset your password. Clicking "Reset" password and
filling out your email will send you a password reset.