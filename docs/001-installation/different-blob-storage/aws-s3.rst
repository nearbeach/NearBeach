AWS S3
======

.. note::

    It is assumed that you have an AWS account.

NearBeach uses Boto3 to connect to AWS. To find more information about Boto3 please go to `their documentation <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html>`_

------------
Instructions
------------

Modify your docker-compose file to include the fields

* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_STORAGE_BUCKET_NAME

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
            volumes:
        ...

Please follow `AWS' guild on setting up S3 IAM credentials <https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-policies-s3.html>`_

AWS Storage Bucket Name can be grabbed from the S3 bucket when creating (or after).