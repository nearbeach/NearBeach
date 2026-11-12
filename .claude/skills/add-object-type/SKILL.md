---
name: add-object-type
description: Bring a NearBeach object (e.g. Task, Requirement, Kanban, RFC, Sprint) onto the new viewset/service/Vue stack, or add a brand-new object type. Use for any "add X as a first-class object" request.
---

# Add or migrate an object type

Read `Architecture.md` first (ObjectAssignment, permissions, request path). Migrated references: Organisation, Project, Customer, Public Link.

## Backend checklist
1. **Model** under `NearBeach/models/` extending `CommonInfo` (soft delete, audit fields, `BigAutoField`). Typed. Export from `models/__init__.py`. Choices go in `utils/enums/` using `gettext_lazy`.
2. **ObjectAssignment:** add a nullable FK to the new model in `models/object_assignment/object_assignment.py`. This is how group access, user assignment and links work.
3. **Permissions:** add a `PermissionSet` field if it needs its own level; register the destination in `utils/api/object_to_permission_set_mapping.py`, and in `utils/api/get_parent_object.py` if it is a child object. Check `utils/dicts/object_dict.py` / `relation_dict.py`.
4. **Migration:** `python3 manage.py makemigrations` (sequential numbering). Review the SQL; never edit applied migrations.
5. **Fixtures:** update `NearBeach/fixtures/NearBeach_basic_setup.json` (and others) incl. ObjectAssignment rows; see `docs/007-misc/fixtures/`.
6. **Serializer, Service, ViewSet, schema docs, routing, tests:** follow the `add-api-endpoint` skill.
7. **Admin/search:** wire into `views/search/` and the potential-object-links data endpoint if the object is linkable.

## Frontend checklist
1. Components in `src/components/<object>/` (`Name.vue`, `Name.spec.ts`, `index.ts`); reuse `object_components/*` (access, documents, notes, link objects, stakeholders).
2. Routes in `src/router/router.ts`; Pinia store updates (`object`, `permissions`, `nav`).
3. Locale keys in `en.json` and `ja.json`.
4. Add to `components/new_object/` if users can create it from the nav.

## Docs
Add or update the user guide under `docs/004-basic-usage/<object>/` and the status note in `Architecture.md` (rewrite-progress banner).

## Verify
`python3 manage.py test`, `mypy NearBeach`, `npm run type-check && npm run lint && npm run test:unit`, then manual QA (see `manual-qa` skill).
