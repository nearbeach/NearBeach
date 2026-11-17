.. _design_error_handling:

==============
Error Handling
==============

Backend
=======

Services return a ``(data, http_status)`` tuple (``ServiceResponse`` in ``NearBeach/services/abstraction/object_services_abstraction.py``). The viewset wraps it in a ``Response``. Errors are expressed as HTTP status codes, not exceptions bubbling to the client:

* Missing object -> ``404`` (raised by ``@object_permission`` when the id is not found).
* Not allowed -> ``PermissionDenied`` -> ``403``.
* Soft-deleted rows are never returned: every queryset filters ``is_deleted=False``.

Frontend
========

Network failures never reject. ``safeFetch`` (``src/composables/safeFetch.ts``) converts a failed ``fetch`` into a synthetic ``503`` whose ``statusText`` is the error message. Callers therefore handle one shape only: switch on ``response.status``.

Every call site follows the same switch:

.. code-block:: ts

    switch (response.status) {
        case 200:   // success state, optionally clear after a timeout
        case 403:   // translated "forbidden" message
        default:    // response.statusText, shown as an error
    }

Failure cases to cover
======================

#. **Failing to get object information** (title, status, ...): show the error; do not render a half-built form.
#. **Failing to get object data** (for example a start date): fall back to the default branch and show ``statusText``.
#. **Failing to create, read or update**: show the inline field status (``info`` -> ``success`` / ``error``); validation uses ``failedValidation`` which *fails by default* when the validation map is undefined.
#. **Unexpected errors**: ``useErrorStore().setError()`` stores the message and opens the global error modal.

Why we do it this way
=====================

* **One shape to handle.** If network failures rejected, every call site would need both a ``try/catch`` and a status ``switch``, and forgetting the ``catch`` would leave the UI stuck on "updating". Converting failures into a 503 means a missed case still lands in the ``default`` branch and shows an error.
* **The server is the source of truth.** Permissions and validity are decided by the backend. The UI reports the outcome (403 gets its own translated message) rather than guessing in advance.
* **Failing closed.** ``failedValidation`` treats an undefined validation map as a failure. A form that forgot to register its rules should block a save, not silently allow one.
* **Inline status over modals.** Field-level ``info`` -> ``success`` / ``error`` feedback tells the user exactly which change did or did not save. The global error modal is kept for the unexpected.
