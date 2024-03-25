.. _first-time-setup:

==============================
First Time Setup for NearBeach
==============================

.. warning::
    For first time login - log into NearBeach normally, NOT through the administration portal


-----------
First Login
-----------

1. Use the login page to log into NearBeach

2. The NearBeach dashboard will load - the administration permissions and groups will be applied to this user and only
this user.


---------------------
Complete your profile
---------------------

The code ``python3 ./manage.py createsuperuser`` does not gather all the information required to create a superuser, i.e. First and Last name. You will need to update this data yourself.

Under the "User" option in the navbar, click on the option "My Profile". This will take you to your profile. Edit your profile appropriately.


-------------------------
Setup User Infrastructure
-------------------------

.. note:: Users will need to be connected to both a Group and Permission set before being able to log in.

Best method of setting NearBeach up for new users is to;

1. Create the required permission sets - please see :ref:`manage-permission-sets`.

2. Create the required groups - please see :ref:`manage-groups`.

3. Finally create the new users and assign them the correct permission sets and groups. Please see :ref:`manage-users`
