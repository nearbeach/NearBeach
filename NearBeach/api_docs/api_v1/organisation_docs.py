"""Swagger/OpenAPI documentation for OrganisationViewSet.

Kept apart from the controller so the view stays thin. The view applies it with
`@extend_schema_view(**PROJECT_SCHEMA)` - keys are the view's method names.

The sub-endpoints (notes, groups, ...) build their `Response` by hand, so drf-spectacular can not
work out what they return - every one is described here with `request=` / `responses=`.
"""
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, OpenApiTypes, extend_schema

from NearBeach.serializers.customer_link_serializer import CustomerLinkSerializer
from NearBeach.serializers.customer_serializer import CustomerSerializer
from NearBeach.serializers.documentation.document_delete_serializer import DocumentDeleteSerializer
from NearBeach.serializers.documentation.document_serializer import DocumentSerializer
from NearBeach.serializers.documentation.file_system_serializer import FileSystemSerializer
from NearBeach.serializers.object_data.note_serializer import NoteSerializer
from NearBeach.serializers.organisation_serializer import (
    OrganisationSerializer,
)

TAGS = ["Organisation"]

# Errors shared by the endpoints. 403 covers "not logged in" as well as "no permission".
_ERRORS = {
    400: OpenApiResponse(description="Invalid input - field errors, or a message such as 'Object does not exist'"),
    403: OpenApiResponse(description="Not logged in, or no permission for this organisation"),
    404: OpenApiResponse(description="Organisation not found"),
}


def _path_id(name, description):
    return OpenApiParameter(
        name=name, type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description=description,
    )


def _responses(success, *errors):
    """The success response(s) plus the listed error codes (400, 403 and 404 unless told otherwise)"""
    errors = errors or (400, 403, 404)
    return {**success, **{code: _ERRORS[code] for code in errors}}


def _doc(summary, description=None, **kwargs):
    return extend_schema(tags=TAGS, summary=summary, description=description, **kwargs)


ORGANISATION_SCHEMA = {
    "list": _doc(
        "List organisations",
        "Paginated list of organisations the user can see. Filter with `?search=` (title or id).",
        responses={
            **_responses({200: OrganisationSerializer(many=True)}, 403),
            404: OpenApiResponse(description="Invalid page number"),
        },
    ),
    "create": _doc(
        "Create a organisation",
        "Requires permission level 3 or above. `group_list` is required and must only contain groups "
        "the user belongs to.",
        responses=_responses({201: OrganisationSerializer}, 400, 403),
    ),
    "retrieve": _doc("Get a organisation", responses=_responses({200: OrganisationSerializer}, 403, 404)),
    "destroy": _doc(
        "Delete a organisation",
        "Soft-deletes the organisation. Requires full permission (level 4).",
        responses=_responses({204: None}, 403, 404),
    ),
    "customer": _doc(
        "List customers linked to a organisation",
        responses=_responses({200: CustomerSerializer(many=True)}, 403, 404),
    ),
    "customer_create": _doc(
        "Link a customer to a organisation",
        "Returns the complete list of customers linked to the organisation.",
        request=CustomerLinkSerializer,
        responses=_responses({201: CustomerSerializer(many=True)}),
    ),
    "customer_delete": _doc(
        "Unlink a customer from a organisation",
        parameters=[_path_id("customer_pk", "ID of the customer link")],
        responses=_responses({204: None}),
    ),
    "documents": _doc(
        "List documents and folders of a organisation",
        responses=_responses({200: FileSystemSerializer}, 403, 404),
    ),
    "documents_create": _doc(
        "Add a document, folder or link to a organisation",
        "`type` decides what is created. `document` needs a `document` file, `link` needs `url_location`.",
        request=DocumentSerializer,
        responses=_responses(
            {
                201: DocumentSerializer,
                413: OpenApiResponse(description="Uploaded file is larger than the maximum upload size"),
            }
        ),
    ),
    "documents_update": _doc(
        "Update a document on a organisation",
        parameters=[_path_id("document_pk", "ID of the document")],
        request=DocumentSerializer,
        responses=_responses({200: DocumentSerializer}),
    ),
    "documents_delete": _doc(
        "Delete a document from a organisation",
        parameters=[_path_id("document_pk", "ID of the document")],
        request=DocumentDeleteSerializer,
        responses=_responses({204: None}),
    ),
    "notes": _doc(
        "List notes of a organisation",
        responses=_responses({200: NoteSerializer(many=True)}, 403, 404),
    ),
    "notes_create": _doc(
        "Create a note on a organisation",
        request=NoteSerializer,
        responses=_responses({201: NoteSerializer}),
    ),
    "notes_update": _doc(
        "Update a note on a organisation",
        "Only the author of a note (or a superuser) can change it.",
        parameters=[_path_id("note_pk", "ID of the note")],
        request=NoteSerializer,
        responses=_responses({200: NoteSerializer}),
    ),
    "notes_delete": _doc(
        "Delete a note from a organisation",
        "Only the author of a note (or a superuser) can delete it.",
        parameters=[_path_id("note_pk", "ID of the note")],
        responses=_responses({204: None}),
    ),
}
