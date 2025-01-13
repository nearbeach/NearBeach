.. _manage-users:

==============
Managing Users
==============

~~~~~~~~~~~~~~~~
Create New Users
~~~~~~~~~~~~~~~~

1. Log into NearBeach as an administrator

2. Choose the "Administration" option in the menu and select the "Users"

3. The "User List" page will load

4. Click the "Create a new User" to start creating a new user


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Assigning Permissions and Groups to Users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Log into NearBeach as an administrator

2. Choose the "Administration" option in the menu and select the "Users"

3. The "User List" page will load

4. Search for the user

5. Click on the appropriate user

6. User information page will load

7. Scroll to the "User List" section

8. Click on the "Add User" button

9. A permission modal will appear. Select the correct permission set and group. Click "Add user" to add the permission sets and groups to the user


.. note::
    To annotate that the user is a team leader for that group - tick the checkbox for that group


~~~~~~~~~~~~~~~~~~~~~~~~~
Removing User from system
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Log into NearBeach as an administrator

2. Choose the "Administration" option in the menu and select the "Users"

3. The "User List" page will load

4. Search for the user

5. Click on the appropriate user

6. User information page will load

7. Scroll to the "User List" section

8. Remove all groups and permissions the user has. This will effectively remove them from the system. They will not be able to log into NearBeach

9. Un-tick the "User Active" tick box and then save

NearBeach does not recommend deleting users. As a delete command will cause a cascade of deletes, and will delete any object that has been modified by the user, or created by them. This will result in data loss.

If the user will need to go through a deletion process, brought on by GDPR (General Data Protection Regulation), we are currently writing functionality to tackle this. The functionality will;

#. Rename the user - and remove any credentials, and reset user's password.

#. Profile pictures will be delete from the blob storage

#. The system will remove any object assignments to the user

#. The system will migrate any "Change User" or "Creation user" records to a user id of choice.

The user is essentially dead information at this point, without the need of a destructive delete.