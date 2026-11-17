.. _design_ajax_patterns:

=============
AJAX Patterns
=============

Rules
=====

* Use ``safeFetch`` from ``src/composables/safeFetch.ts``; never raw ``fetch`` for state-changing calls.
* Send ``X-CSRFTOKEN`` from ``getCsrfToken()`` and ``Content-Type: application/json``.
* URLs are ``/api/v1/<destination>/<id>/``. Use ``PATCH`` with only the changed field for single-field updates.
* Show progress to the user: set an ``info`` state before the call, then ``success`` or ``error`` after it.
* Handle the response with a ``switch`` on ``response.status`` (see :ref:`design_error_handling`).

Reference implementation
========================

``src/components/object_components/object_priority/ObjectPriority.vue``: a ``watch`` on the model, an optimistic store patch, a ``PATCH`` through ``safeFetch``, then a status switch.

Why we do it this way
=====================

* **Optimistic store updates.** The Pinia store is patched before the request returns so the UI feels instant and sibling components (which subscribe to the store) update together. The status text tells the user if the save later fails.
* **Single-field ``PATCH``.** Sending only the changed field means two people editing different fields of one object do not overwrite each other, and each field component stays self-contained.
* **Fetch lives in the component that owns the field.** Each object component (priority, assigned users, links, ...) is a complete unit: UI, save and error feedback together. It can be dropped onto any object page, driven by ``objectStore.destination`` and ``objectStore.id``, without a shared API layer to extend.
* **CSRF and JSON headers are always the same**, so they are centralised in ``getCsrfToken`` and ``safeFetch`` instead of being re-invented per call.
