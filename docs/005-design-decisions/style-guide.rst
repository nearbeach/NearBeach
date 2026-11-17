.. _design_style_guide:

===========
Style Guide
===========

Python
======

* PEP 8, formatted with black.
* New models and services are fully type-annotated (``mypy NearBeach``).
* Service files are PascalCase (``ProjectService.py``); API views ``*_api_view.py``; schema constants ``XXX_SCHEMA``; destinations are lowercase singular (``"project"``).
* Filter ``is_deleted=False`` on every queryset.

TypeScript / Vue
================

* ``<script setup lang="ts">``; small single-file components; Pinia for shared state.
* No hard-coded user-visible strings.
* Keep accessibility intact: skip links, labels, focus order, contrast.
* Before finishing: ``npm run type-check``, ``npm run lint``, ``npm run test:unit``, ``npm run format``.
