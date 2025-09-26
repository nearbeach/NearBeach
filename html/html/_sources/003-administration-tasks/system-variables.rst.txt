.. _system-variables:

System Variables
################

The following django system variables are required by NearBeach;

* SECRET_KEY
* ALLOWED_HOSTS
* CSRF_TRUSTED_URLS
* DB_DATABASE
* DB_ENGINE
* DB_HOST
* DB_PASSWORD
* DB_PORT
* DB_USER

Blob Storage
============

Azure
-----

AZURE_STORAGE_CONNECTION_STRING
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Please refer to the Microsoft Azure documentation for setting up and obtaining the connection string.`_

Example:

* `AZURE_STORAGE_CONNECTION_STRING=defaultendpointsprotocol=https;accountname=accountname;accountkey=accountkey;endpointsuffix=core.windows.net/`

AZURE_STORAGE_CONTAINER_NAME
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The name of the Azure Blob storage

Example:

* `AZURE_STORAGE_CONTAINER_NAME=blobstorage`


S3/Minio
--------

`For setup of AWS S3 connections, please refer to the AWS IAMS documentation`_

`For setup of Minio connections, please refer to the Minio Access Control documentation`_

`For any Boto3 information, please refer to the Boto3 documentation`_

AWS_ACCESS_KEY_ID
^^^^^^^^^^^^^^^^^

This references the Access Key Id

Example:

* `AWS_ACCESS_KEY_ID=hfOlT4DrY9VkyiMLCKn9`


AWS_SECRET_ACCESS_KEY
^^^^^^^^^^^^^^^^^^^^^

This references the Secret Access Key

Example:

* `AWS_SECRET_ACCESS_KEY=sET3GI24o3sn3mFiFbIMUGyz9CrgdqIOot011THy`

AWS_STORAGE_BUCKET_NAME
^^^^^^^^^^^^^^^^^^^^^^^

This references the S3 Bucket name

Example:

* `AWS_STORAGE_BUCKET_NAME=NearBeachBucket`

AWS_S3_ENDPOINT_URL
^^^^^^^^^^^^^^^^^^^

This references the S3 Endpoint url

Example:

* `AWS_S3_ENDPOINT_URL=http://localhost:9000`
* `AWS_S3_ENDPOINT_URL=https://s3.bucket.nearbeach.cloudstorage.com`

Database
========

DB_DATABASE
-----------

`More information on Django Databases can be found on their documentation.`_ This represent the name of the database.

No default is set, user will need to set.

Example:

* `DB_DATABASE=nearbeach_db`


DB_ENGINE
---------

`More information on Django Databases can be found on their documentation.`_ This represent the database engine.

No default is set, user wil need to set.

Example:

* `DB_ENGINE=postgresql` <- Connects to a Postgres Database
* `DB_ENGINE=mysql` <- Connects to either a MySQL or MariaDb database
* `DB_ENGINE=` <- Connects to a Postgres Database
* `DB_ENGINE=oracle` <- Connects to an Oracle Database


DB_HOST
-------

`More information on Django Databases can be found on their documentation.`_ This represents the location of the database.

No default is set, user wil need to set.

Example:

* `DB_HOST=127.0.0.1` <- Connects to a database at localhost
* `DB_HOST=nearbeach-db.cloudservices.hosting` <- Connects to a database at nearbeach-db.cloudservices.hosting

DB_PASSWORD
-----------

`More information on Django Databases can be found on their documentation.`_ This is the password for the database.

No default is set, user wil need to set.

Example:

* `DB_PASSWORD=mysecretpassword`

DB_PORT
-------

`More information on Django Databases can be found on their documentation.`_ This represent the port for the database.

No default is set, user wil need to set.

Example:

* `DB_PORT=3306`
* `DB_PORT=5432`

DB_USER
-------
`More information on Django Databases can be found on their documentation.`_ This is the username for the database.

No default is set, user wil need to set.

Example:

* `DB_USER=nearbeach_db_user`


Django System Variables
=======================

SECRET_KEY
----------

`More information can be located on the Django Documentation.`_ We recommend setting up this variable using the `following information from this Humberto's blog`_


ALLOWED_HOSTS
-------------

`More information can be located on the Django Documentation.`_

Allowed Hosts should reference which URLs will be connected to the NearBeach system. If there are multiple URLs, each
url can be separated by a commar. Do not include the http or port number

Default will allow ALL hosts - we do not recomment

Example:

* `- ALLOWED_HOST=demo.nearbeach.org`
* `- ALLOWED_HOST=demo.nearbeach.org,test.nearbeach.org`
* `- ALLOWED_HOST=localhost,127.0.0.1`


CSRF_TRUSTED_URLS
-----------------

`More information can be located on the Django Documentation.`_

Csrf trusted urls should reference the exact urls form submissions will be coming from. If there are multiple URLs, each
url can be separated by a commar. Please include the http/https and, if required, port number.

Default will allow ALL hosts - we do not recommend.

Example:

* `CSRF_TRUSTED_URLS=https://demo.nearbeach.org`
* `CSRF_TRUSTED_URLS=https://demo.nearbeach.org,https://test.nearbeach.org:8080`
* `CSRF_TRUSTED_URLS=http://localhost:8000,http://127.0.0.1:8000`


DEBUG
-----

Default will be false. Only use this on production to debug an issue.

DOCUMENTATION_CLEAN_UP
----------------------

Used to notify the system to run periodic checks to clean up the Blob storage from any documenation that does not current
have a link to any object within NearBeach. It is designed so that old documentation that has been removed, is cleaned
from the BLOB storage.

Default will be false.

Example:

* `DOCUMENTATION_CLEAN_UP=True`
* `DOCUMENTATION_CLEAN_UP=False`

DOCUMENTATION_CLEAN_AFTER_DAYS
------------------------------

Used to notify the system the PERIOD on which to run the document clean up process.

Default will be 90 days

Example:

* `DOCUMENTATION_CLEAN_AFTER_DAYS=120` <- cleaned up every 120 days
* `DOCUMENTATION_CLEAN_AFTER_DAYS=365` <- cleaned up once a year
* `DOCUMENTATION_CLEAN_AFTER_DAYS=7` <- cleaned up each week


MAX_FILE_SIZE_UPLOAD
--------------------

The maximum size for a file to be uploaded in bytes.

Default will be 104857600 bytes (104mb)

Example:

* `MAX_FILE_SIZE_UPLOAD=1048` <- 1kb
* `MAX_FILE_SIZE_UPLOAD=1048000` <- 1mb
* `MAX_FILE_SIZE_UPLOAD=1048000000` <- 1Gb

+----------------------+-----------------+---------------+
| Human Readable Value | MAX_FILE_UPLOAD | Notes         |
+======================+=================+===============+
| 100MB                | 104857600       | Default Value |
+----------------------+-----------------+---------------+
| 10MB                 | 10485760        |               |
+----------------------+-----------------+---------------+
| 1GB                  | 1048576000      |               |
+----------------------+-----------------+---------------+


SESSION_COOKIE_AGE
------------------

`More information can be located on the Django Documentation.`_

Used to define how long a session cookie will last.

Default: 1209600 seconds (2 weeks)

Example:

* `SESSION_COOKIE_AGE=1209600` <- 2 weeks
* `SESSION_COOKIE_AGE=3360` <- 24 hours

+----------------------+-----------------+-------------------+
| Human Readable Value | MAX_FILE_UPLOAD | Notes             |
+======================+=================+===================+
| 2 weeks              | 1209600         | Default Value     |
+----------------------+-----------------+-------------------+
| 1 hour               | 3600            | Recommended Value |
+----------------------+-----------------+-------------------+
| 30 min               | 1800            |                   |
+----------------------+-----------------+-------------------+

SESSION_SAVE_EVERY_REQUEST
--------------------------

`More information can be located on the Django Documentation.`_

Default will be false.

Example:

* `DOCUMENTATION_CLEAN_UP=True`
* `DOCUMENTATION_CLEAN_UP=False`


Email/SMTP
==========

`More information on Django SMTP can be found on their documentation`_

SMTP_EMAIL_HOST
---------------

The SMTP host

Example:

* `SMTP_EMAIL_HOST=email-smtp.us-east-2.amazonaws.com`
* `SMTP_EMAIL_HOST=smtp.gmail.com`

SMTP_EMAIL_PORT
---------------

SMTP Email Port

Example:

* `SMTP_EMAIL_PORT=465`


SMTP_EMAIL_HOST_USER
--------------------

SMTP Email host user

Example:

* `SMTP_EMAIL_USER=smtpuser`

SMTP_EMAIL_HOST_PASSWORD
------------------------

SMTP Email Host password

Example:

* `SMTP_EMAIL_PASSWORD=secretPassword`



.. _More Information can be located on the Django Documentation.: https://docs.djangoproject.com/en/dev/ref/settings/
.. _following information from this Humberto's blog: https://humberto.io/blog/tldr-generate-django-secret-key/
.. _More information on Django Databases can be found on their documentation.: https://docs.djangoproject.com/en/dev/ref/databases/
.. _Please refer to the Microsoft Azure documentation for setting up and obtaining the connection string.: https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal
.. _For setup of AWS S3 connections, please refer to the AWS IAMS documentation: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console
.. _For setup of Minio connections, please refer to the Minio Access Control documentation: https://docs.min.io/enterprise/aistor-object-store/administration/iam/access/
.. _For any Boto3 information, please refer to the Boto3 documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration
.. _More information on Django SMTP can be found on their documentation: https://docs.djangoproject.com/en/5.2/ref/settings/