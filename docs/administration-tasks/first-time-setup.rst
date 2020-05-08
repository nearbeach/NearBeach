First Time Setup for NearBeach
==============================

.. note::
    The first login for NearBeach will setup the administration group and permission set. Please log into NearBeach normally and not through the administration portal

.. warning::
    For first time login - log into NearBeach normally, NOT through the administration portal

-----------
First Login
-----------

1. Use the login page to log into NearBeach
    .. image:: images/first-time-setup-001.jpg

2. The NearBeach dashboard will load - the following alerts will notify you which tasks are required to be completed.
    .. image:: images/first-time-setup-002.jpg


^^^^^^^^^^^^^^^^^^^^^
Complete your profile
^^^^^^^^^^^^^^^^^^^^^

The code ``python3 ./manage.py createsuperuser`` does not gather all the information required to create a superuser, i.e. First and Last name. You will need to update this data yourself.

Click on the "My Profile" option in the Navigation bar. This will take you to your profile. Edit your profile appropriately.


^^^^^^^^^^^^^^^^^^^^^^^^
Setup of Permission Sets
^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
    Permission Sets in NearBeach give you the ability to classify how much access a particular user can have to certain objecst, i.e. Projects and Tasks. The permission sets can be stacked on top of each other.

    Users can also have different permissions between each group. For example, a user might have basic user access to group_A, however only have read only access to group_B.

