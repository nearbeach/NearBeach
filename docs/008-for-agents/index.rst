.. _for_agents:

=========================
NearBeach for AI Agents
=========================

This section gives AI agents and the developers who build them the context needed to understand and use NearBeach. Coding agents working *inside* the repository should read ``AGENTS.md`` and ``Architecture.md`` at the repository root instead.

Domain model
============

NearBeach manages the following objects:

* **Organisations** and **Customers** - who the work is for.
* **Projects**, **Tasks**, **Requirements** (and Requirement Items), **Kanban Boards** (with Cards), **Request for Changes** (with Change Tasks) and **Sprints** - the work itself.
* **Documents**, **Notes** and **Tags** - supporting material attached to objects.
* **Groups**, **Permission Sets** and **Users** - who can see and do what.

.. note:: The 0.32 development branch is rewriting the application. At the time of writing, Organisations, Projects, Customers and Public Links are available through the new API; other objects follow.

How objects connect
===================

A single assignment table links everything. A row can grant a **group** access to an object, assign a **user** to an object, or **link** two objects with a relationship (block, duplicate, relate or sub-object).

Permissions
===========

A user's access to an object is the combination of:

#. The user's group membership - the group must be assigned to the object.
#. The permission level the user's permission set grants for that object type: 0 none, 1 read, 2 edit, 3 add and edit, 4 full.

Some areas (notes, documents, tags) have additive permissions on top of the base level. Permissions are enforced on the server for every request.

Using the API
=============

* Base path: ``/api/v1/``.
* The OpenAPI schema is served at ``/api/v1/schema/`` and interactive documentation at ``/api/v1/docs/``. A generated copy is kept in the repository as ``schema.yml``.
* Authentication: session, token (knox) or OAuth2 - see :doc:`/003-administration-tasks/oauth2-api` and :doc:`/003-administration-tasks/api`.
* Deleted objects are soft-deleted and are not returned by the API.
* Requests for objects that do not exist return 404; requests for objects the user may not access are rejected by the permission checks.

Machine-readable index
======================

An ``llms.txt`` file is published at the root of this documentation site.
