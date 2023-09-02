.. _azure:

======================
Use Azure Blob Storage
======================

.. note::

    It is assumed that you have an Azure account.

NearBeach uses Azure's own toolset to connect to Azure Blob storage. `For more information please visit Microsoft's documentation <https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python>`_

------------
Instructions
------------

Modify your docker-compose file to include the fields

* AZURE_STORAGE_CONNECTION_STRING
* AZURE_STORAGE_CONTAINER_NAME

The following is an example snippet of code

.. code-block:: bash

    version: '3'

    services:
        ...
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
            - AZURE_STORAGE_CONNECTION_STRING=<<Please fill>>
            - AZURE_STORAGE_CONTAINER_NAME=<<Please fill>>
            volumes:
        ...

`How to get Storage Connection String <https://learn.microsoft.com/en-us/azure/storage/common/storage-account-get-info?tabs=portal>`_

The Azure Storage container name is the Azure storage container.