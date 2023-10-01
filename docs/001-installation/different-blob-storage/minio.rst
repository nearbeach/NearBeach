.. _minio:

======================
Use Minio Blob Storage
======================

.. note::

    It is assumed that you have a Minio account.

NearBeach uses Boto3 to connect to Minio. To find more information about Boto3 please go to `their documentation <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html>`_

------------
Instructions
------------

Modify your docker-compose file to include the fields

* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_STORAGE_BUCKET_NAME
* AWS_S3_ENDPOINT_URL

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
            - AWS_ACCESS_KEY_ID=<<Please fill>>
            - AWS_SECRET_ACCESS_KEY=<<Please fill>>
            - AWS_STORAGE_BUCKET_NAME=<<Please fill>>
            - AWS_S3_ENDPOINT_URL=<<Please fill>>
            volumes:
        ...


Please follow any Minio instructions on how to obtain the Access Key and Secret Access Key.

The storage bucket name should match the bucket name created in the minio client.

The S3 endpoint url is the API endpoint for minio. i.e. localhost:9000