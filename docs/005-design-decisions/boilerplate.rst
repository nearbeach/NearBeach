.. _design_boilerplate:

===========
Boilerplate
===========

New Vue component
=================

One folder per component under ``src/components/<feature>/``:

* ``Name.vue`` using ``<script setup lang="ts">``
* ``Name.spec.ts`` (Vitest)
* ``index.ts`` barrel

Strings go through ``useI18n()`` with keys in both ``src/locales/en.json`` and ``ja.json``.

New API endpoint
================

#. Viewset action with ``@apply_schema`` and the permission decorator.
#. Service subclassing ``ObjectServiceAbstraction`` (fully type-annotated, returns ``(data, status)``).
#. Serializer.
#. Tests for every role folder in ``NearBeach/tests/tests_api/test_permissions/``.
