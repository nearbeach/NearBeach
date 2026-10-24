"""Swagger/OpenAPI documentation for ProjectViewSet.

Kept apart from the controller so the view stays thin. The view applies it with
`@extend_schema_view(**PROJECT_SCHEMA)` - keys are the view's method names.
"""
from drf_spectacular.utils import extend_schema

TAGS = ["Projects"]


def _doc(summary, description=None, **kwargs):
    return extend_schema(tags=TAGS, summary=summary, description=description, **kwargs)


PROJECT_SCHEMA = {
    "list": _doc("List projects", "Paginated list of projects the user can see."),
    "create": _doc("Create a project", "Requires permission level 3 or above."),
    "retrieve": _doc("Get a project"),
    "partial_update": _doc("Update a project"),
    "destroy": _doc("Delete a project", "Soft-deletes the project."),
    "customer": _doc("List customers linked to a project"),
    "customer_create": _doc("Link a customer to a project"),
    "customer_delete": _doc("Unlink a customer from a project"),
    "documents": _doc("List documents and folders of a project"),
    "documents_create": _doc("Add a document, folder or link to a project"),
    "documents_update": _doc("Update a document on a project"),
    "documents_delete": _doc("Delete a document from a project"),
    "groups_list": _doc("List groups of a project"),
    "groups_list_create": _doc("Add a group to a project"),
    "groups_list_delete": _doc("Remove a group from a project"),
    "link_list": _doc("List links of a project"),
    "link_list_create": _doc("Create a link on a project"),
    "link_list_update": _doc("Update a link on a project"),
    "link_list_delete": _doc("Delete a link from a project"),
    "notes": _doc("List notes of a project"),
    "notes_create": _doc("Create a note on a project"),
    "notes_update": _doc("Update a note on a project"),
    "notes_delete": _doc("Delete a note from a project"),
    "organisation": _doc("Get the organisation linked to a project"),
    "organisation_create": _doc("Link an organisation to a project"),
    "organisation_delete": _doc("Unlink the organisation from a project"),
    "public_link": _doc("List public links of a project"),
    "public_link_create": _doc("Create a public link for a project"),
    "public_link_update": _doc("Update a public link of a project"),
    "public_link_delete": _doc("Delete a public link of a project"),
    "sprint": _doc("List sprints linked to a project"),
    "sprint_create": _doc("Link a sprint to a project"),
    "sprint_delete": _doc("Unlink a sprint from a project"),
    "users_list_create": _doc("Add a user to a project"),
    "users_list_delete": _doc("Remove a user from a project"),
}
