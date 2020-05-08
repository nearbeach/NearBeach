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


^^^^^^^^^^^^^^^^
Create New Users
^^^^^^^^^^^^^^^^

1. Log into NearBeach as an administrator

2. Choose the "Administration" option in the menu and select the "Users"

3. The "User List" page will load

4. Click the "Create a new User" to start creating a new user

.. note::
    Permission and Groups are assigned in a different module


^^^^^^^^^^^^^^^^^^^^^^^^
Setup of Permission Sets
^^^^^^^^^^^^^^^^^^^^^^^^

1. Log into NearBeach as an administrator

2. Choose the "Administration" option in the menu and select the "Permission Sets"

3. The "Permission Set List" page will load

4. Click the "Create a new Permission Set" to start creating a new permission list

.. note::
    Permission Sets in NearBeach give you the ability to classify how much access a particular user can have to certain objecst, i.e. Projects and Tasks. The permission sets can be stacked on top of each other.

    Users can also have different permissions between each group. For example, a user might have basic user access to group_A, however only have read only access to group_B.

1. Log into NearBeach as an administrator

2. Choose the "Administration" option in the menu and select the "Permission Sets"

3. The "Permission Set List" page will load

4. Click the "Create a new Permission Set" to start creating a new permission list

.. note::
    There are 4 different levels of permissions;

    - 'No Permission' - the user will not have any permissions
    - 'Read Only' - the user will only have read only access
    - 'Edit Only' - user will be able to edit already existing objects, i.e. Projects
    - 'Add and Edit' - user will be able to create objects, i.e. New Projects
    - 'Full Permission' - users will be able to do the above permissions and delete objects.

.. note::
    The permissions are broken up into three sections;

    - 'Administration Permissions' - This contains any administration permissions. It is not recommended granting these to any basic users.
    - 'Normal Permissions' - Are used to determine a user's permission to objects and different modules within said objects.
    - 'Addon Permissions' - These are extra permissions designed for read only users.



^^^^^^^^^^^^^^^^^^
Create User Groups
^^^^^^^^^^^^^^^^^^

.. note::
    Each group will require a unique name.

.. note::
    Users can be in multiple groups, with different permissions to each group

.. note::
    Permission sets can be stacked for users within that group. i.e. Read Only user can have extra permissions stacked on top.

1. Log into NearBeach as an administrator

2. Choose the "Administration" option in the menu and select the "Groups"

3. The "Group List" page will load

4. Click the "Create a new Group" to start creating a new permission list

Once the group has been created, you will be able to add permission sets + users. User's have to be connected to a permission set.

.. note::
    At least one user in the group should be tagged as group leader.
