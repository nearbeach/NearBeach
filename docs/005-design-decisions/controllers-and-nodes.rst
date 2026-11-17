.. _design_controllers_and_nodes:

=====================
Controllers and Nodes
=====================

Why controllers are small
=========================

A viewset does three things only: apply the schema (``@apply_schema``), enforce permission (``@object_permission`` / ``@destination_permission``), and delegate to a Service. Business logic lives in ``NearBeach/services/`` and shaping of data in ``NearBeach/serializers/``. This keeps permission checks uniform and lets services be tested without HTTP.

.. code-block:: text

    ViewSet -> permission decorator -> Service (returns data, status) -> Serializer

Why there are many nodes
========================

.. note:: We are using the work 'node' as an action on a viewset

Each viewset exposes many endpoints, because one object has many independently editable facets: core fields, notes, links, assigned users, group access, stakeholders. We chose many narrow endpoints over a few wide ones:

* **Permissions are per facet.** Additive permissions (``project_note`` and similar) extend the base level, so each facet needs its own decorator and level.
* **Narrow endpoints are simple to document and test.** Each has its own ``@apply_schema`` entry and its own role tests.
* **Each stays tiny.** Because logic lives in the Service, adding an endpoint costs a few lines in the viewset, so the file grows in count of endpoints rather than in complexity.

The accepted trade-off is longer viewset files and more routes to maintain, in return for simple, individually testable and individually permissioned actions.
