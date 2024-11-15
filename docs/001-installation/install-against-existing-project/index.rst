.. _install-against-existing-project:

================================
Install Against Existing Project
================================

The following documentation is a guide on how to install NearBeach against an existing software. aka
you would like to use NearBeach with your own project.

-----------
Assumptions
-----------

* User has already setup email configuration
* User has already setup database configuration
* User has already setup the security options for SECURE_SSL_REDIRECT etc.
* User has already setup the static url options
* User is not using any of the media/private urls

-----------------
Helicopter Method
-----------------

* Insert "NearBeach" into your requirements.txt file
* Install "NearBeach" using pip (or equivalent)
* Add NearBeach to the settings.py file under the Installed Apps
* Add the NearBeach's calls to the context processors
* Add all private and media settings
* Add the NearBeach url to urls
* Migrate the NearBeach migrations
* User will create a permission set in the backend


------
Method
------

#. Open your requirements.txt file, and insert NearBeach on a new line

#. Using pip (or equivalent), install NearBeach

#. Open your "settings.py" file and navigate to the "Installed Apps" section.

    .. image:: install-apps.png
      :alt: Picture of the installed apps within the settings

#. Add "NearBeach.apps.NearBeachConfig" within the array of installed apps. Please see image

    .. image:: templates.png
        :alt: Picture of the templates within the settings

#. Add the following two lines into the context_processors within the Templates

    .. code-block:: bash

            'NearBeach.context_processors.django_version',
            'NearBeach.context_processors.nearbeach_version',

#. At the bottom of the settings.py file, insert the following code

    .. code-block:: bash

        PRIVATE_MEDIA_URL = '/private/'
        PRIVATE_MEDIA_ROOT = '/private'
        PRIVATE_MEDIA_SERVER = 'ApacheXSendfileServer'
        MEDIA_URL = '/media/'
        MEDIA_ROOT = os.path.join(BASE_DIR,'media/')


    This is for NearBeach's document upload process.

#. At the top of the "settings.py" file, please add the following import statement

    .. code-block:: bash

        import os

#. Open your urls.py file, and include the following import

    .. code-block:: bash

        from django.urls import path, include

    Note, you could just appear the "include" on the existing line

#. In the urls.py file, add the following line within the urlpatters array

    .. code-block:: bash

        path('NearBeach/', include('NearBeach.urls')),

#. In your terminal, migrate the files

    .. code-block:: bash

        python3 ./manage.py migrate NearBeach


NearBeach should be setup. You can reach it using /NearBeach/ on your site.

.. note::

    You will need to manually create the Permission Set for the administration. The first Permission Set
    created in NearBeach can not be edited from the front end.

--------
Optional
--------

Add the following code to your "admin.py" file, so tables can appear in the Django Admin

.. code-block:: bash

    from django.contrib import admin

    # Register your models here.
    from .models import (
        Bug,
        BugClient,
        ChangeTask,
        ChangeTaskBlock,
        Customer,
        Document,
        DocumentPermission,
        Folder,
        GroupPermission,
        Group,
        KanbanBoard,
        KanbanCard,
        KanbanColumn,
        KanbanLevel,
        ListOfBugClient,
        ListOfProjectStatus,
        ListOfRequirementItemStatus,
        ListOfRequirementItemType,
        ListOfRequirementStatus,
        ListOfRequirementType,
        ListOfRFCStatus,
        ListOfTaskStatus,
        ListOfTitle,
        Notification,
        ObjectAssignment,
        ObjectNote,
        ObjectTemplate,
        Organisation,
        PermissionSet,
        Project,
        PublicLink,
        RequestForChange,
        RequestForChangeGroupApproval,
        Requirement,
        RequirementItem,
        ScheduledObject,
        Sprint,
        SprintAuditTable,
        SprintObjectAssignment,
        Tag,
        TagAssignment,
        Task,
        UserGroup,
        UserJob,
    )

    admin.site.register(Bug)
    admin.site.register(BugClient)
    admin.site.register(ChangeTask)
    admin.site.register(ChangeTaskBlock)
    admin.site.register(Customer)
    admin.site.register(Document)
    admin.site.register(DocumentPermission)
    admin.site.register(Folder)
    admin.site.register(GroupPermission)
    admin.site.register(Group)
    admin.site.register(KanbanBoard)
    admin.site.register(KanbanCard)
    admin.site.register(KanbanColumn)
    admin.site.register(KanbanLevel)
    admin.site.register(ListOfBugClient)
    admin.site.register(ListOfProjectStatus)
    admin.site.register(ListOfRequirementItemStatus)
    admin.site.register(ListOfRequirementItemType)
    admin.site.register(ListOfRequirementStatus)
    admin.site.register(ListOfRequirementType)
    admin.site.register(ListOfRFCStatus)
    admin.site.register(ListOfTaskStatus)
    admin.site.register(ListOfTitle)
    admin.site.register(Notification)
    admin.site.register(ObjectAssignment)
    admin.site.register(ObjectNote)
    admin.site.register(ObjectTemplate)
    admin.site.register(Organisation)
    admin.site.register(PermissionSet)
    admin.site.register(Project)
    admin.site.register(PublicLink)
    admin.site.register(ScheduledObject)
    admin.site.register(Sprint)
    admin.site.register(SprintAuditTable)
    admin.site.register(SprintObjectAssignment)
    admin.site.register(RequestForChange)
    admin.site.register(RequestForChangeGroupApproval)
    admin.site.register(Requirement)
    admin.site.register(RequirementItem)
    admin.site.register(Tag)
    admin.site.register(TagAssignment)
    admin.site.register(Task)
    admin.site.register(UserGroup)
    admin.site.register(UserJob)