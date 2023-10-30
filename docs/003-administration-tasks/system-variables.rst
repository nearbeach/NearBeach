.. _system-variables:

================
System Variables
================

--------------------
MAX_FILE_SIZE_UPLOAD
--------------------

Max file size upload determines how large a file a user can upload. By default it is set at 100MB.

Examples of different values

+----------------------+-----------------+---------------+
| Human Readable Value | MAX_FILE_UPLOAD | Notes         |
+======================+=================+===============+
| 100MB                | 104857600       | Default Value |
+----------------------+-----------------+---------------+
| 10MB                 | 10485760        |               |
+----------------------+-----------------+---------------+
| 1GB                  | 1048576000      |               |
+----------------------+-----------------+---------------+

------------------
SESSION_COOKIE_AGE
------------------

Sesseion cookie age is a Django setting attribute - https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-SESSION_COOKIE_AGE
Use this setting to automatically log a user out after x amount of seconds

Example values

+----------------------+-----------------+-------------------+
| Human Readable Value | MAX_FILE_UPLOAD | Notes             |
+======================+=================+===================+
| 2 weeks              | 1209600         | Default Value     |
+----------------------+-----------------+-------------------+
| 1 hour               | 3600            | Recommended Value |
+----------------------+-----------------+-------------------+
| 30 min               | 1800            |                   |
+----------------------+-----------------+-------------------+

--------------------------
SESSION_SAVE_EVERY_REQUEST
--------------------------

A django setting attribute - https://docs.djangoproject.com/en/4.2/ref/settings/#session-save-every-request
Used to determine if the cookies are refreshed every single time the user utilises NearBeach. We recommend True
