"""Swagger/OpenAPI documentation for RequirementViewSet.

Kept apart from the controller so the view stays thin. The view applies it with
`@extend_schema_view(**REQUIREMENT_SCHEMA)` - keys are the view's method names.

The sub-endpoints (notes, groups, ...) build their `Response` by hand, so drf-spectacular can not
work out what they return - every one is described here with `request=` / `responses=`.
"""
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, OpenApiTypes, extend_schema

from NearBeach.serializers.audit_log_serializer import AuditLogSerializer
from NearBeach.serializers.customer_link_serializer import CustomerLinkSerializer
from NearBeach.serializers.customer_serializer import CustomerSerializer
from NearBeach.serializers.documentation.document_delete_serializer import DocumentDeleteSerializer
from NearBeach.serializers.documentation.document_serializer import DocumentSerializer
from NearBeach.serializers.documentation.file_system_serializer import FileSystemSerializer
from NearBeach.serializers.group_and_user_serializer import GroupAndUserSerializer
from NearBeach.serializers.group_list_serializer import GroupListSerializer
from NearBeach.serializers.object_data.link_serializer import LinkSerializer
from NearBeach.serializers.object_data.note_serializer import NoteSerializer
from NearBeach.serializers.organisation_link_serializer import OrganisationLinkSerializer
from NearBeach.serializers.requirement_serializer import (
    RequirementDetailSerializer,
    RequirementPatchSerializer,
    RequirementSerializer,
)
from NearBeach.serializers.public_link_serializer import PublicLinkSerializer
from NearBeach.serializers.sprint_serializer import SprintSerializer
from NearBeach.serializers.user_list_serializer import UserListSerializer

TAGS = ["Requirements"]

# Errors shared by the endpoints. 403 covers "not logged in" as well as "no permission".
_ERRORS = {
    400: OpenApiResponse(description="Invalid input - field errors, or a message such as 'Object does not exist'"),
    403: OpenApiResponse(description="Not logged in, or no permission for this requirement"),
    404: OpenApiResponse(description="Requirement not found"),
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


REQUIREMENT_SCHEMA = {
    "list": _doc(
        "List requirements",
        "Paginated list of requirements the user can see. Filter with `?search=` (title or id).",
        responses={
            **_responses({200: RequirementSerializer(many=True)}, 403),
            404: OpenApiResponse(description="Invalid page number"),
        },
    ),
    "create": _doc(
        "Create a requirement",
        "Requires permission level 3 or above. `group_list` is required and must only contain groups "
        "the user belongs to.",
        responses=_responses({201: RequirementSerializer}, 400, 403),
    ),
    "retrieve": _doc("Get a requirement", responses=_responses({200: RequirementDetailSerializer}, 403, 404)),
    "partial_update": _doc(
        "Update a requirement",
        "Send only the fields to change. Groups, users and organisation have their own endpoints, and "
        "`status` is the id of a requirement status. The response is the updated requirement in this same shape. "
        "`meta_data` is merged into the stored JSON object (JSON Merge Patch): keys you send are added or "
        "updated, keys you leave out are kept, and a key set to `null` is deleted. It must be an object and "
        "the saved result is limited to 64KB.",
        request=RequirementPatchSerializer,
        responses=_responses({200: RequirementPatchSerializer}),
    ),
    "destroy": _doc(
        "Delete a requirement",
        "Soft-deletes the requirement. Requires full permission (level 4).",
        responses=_responses({204: None}, 403, 404),
    ),
    "audit": _doc(
        "List the audit history of a requirement",
        "Paginated, newest first. Each entry says who made the change and when, and `changes` holds every "
        "field that moved as `{field: {old, new}}`. Requires read permission. Entries are removed after the "
        "configured retention period.",
        responses=_responses({200: AuditLogSerializer(many=True)}, 403, 404),
    ),
    "customer": _doc(
        "List customers linked to a requirement",
        responses=_responses({200: CustomerSerializer(many=True)}, 403, 404),
    ),
    "customer_create": _doc(
        "Link a customer to a requirement",
        "Returns the complete list of customers linked to the requirement.",
        request=CustomerLinkSerializer,
        responses=_responses({201: CustomerSerializer(many=True)}),
    ),
    "customer_delete": _doc(
        "Unlink a customer from a requirement",
        parameters=[_path_id("customer_pk", "ID of the customer link")],
        responses=_responses({204: None}),
    ),
    "documents": _doc(
        "List documents and folders of a requirement",
        responses=_responses({200: FileSystemSerializer}, 403, 404),
    ),
    "documents_create": _doc(
        "Add a document, folder or link to a requirement",
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
        "Update a document on a requirement",
        parameters=[_path_id("document_pk", "ID of the document")],
        request=DocumentSerializer,
        responses=_responses({200: DocumentSerializer}),
    ),
    "documents_delete": _doc(
        "Delete a document from a requirement",
        parameters=[_path_id("document_pk", "ID of the document")],
        request=DocumentDeleteSerializer,
        responses=_responses({204: None}),
    ),
    "groups_list": _doc(
        "List groups of a requirement",
        responses=_responses({200: GroupAndUserSerializer}, 403, 404),
    ),
    "groups_list_create": _doc(
        "Add a group to a requirement",
        "Returns the updated group and user lists.",
        request=GroupListSerializer,
        responses=_responses({201: GroupAndUserSerializer}),
    ),
    "groups_list_delete": _doc(
        "Remove a group from a requirement",
        "The last group of a requirement can not be removed. Returns the updated group and user lists.",
        parameters=[_path_id("group_pk", "ID of the group")],
        responses=_responses({200: GroupAndUserSerializer}),
    ),
    "link_list": _doc(
        "List links of a requirement",
        responses=_responses({200: LinkSerializer(many=True)}, 403, 404),
    ),
    "link_list_create": _doc(
        "Create a link on a requirement",
        request=LinkSerializer,
        responses=_responses({201: LinkSerializer}),
    ),
    "link_list_update": _doc(
        "Update a link on a requirement",
        parameters=[_path_id("link_pk", "ID of the link")],
        request=LinkSerializer,
        responses=_responses({200: OpenApiResponse(description="Link updated")}),
    ),
    "link_list_delete": _doc(
        "Delete a link from a requirement",
        parameters=[_path_id("link_pk", "ID of the link")],
        responses=_responses({204: None}),
    ),
    "notes": _doc(
        "List notes of a requirement",
        responses=_responses({200: NoteSerializer(many=True)}, 403, 404),
    ),
    "notes_create": _doc(
        "Create a note on a requirement",
        request=NoteSerializer,
        responses=_responses({201: NoteSerializer}),
    ),
    "notes_update": _doc(
        "Update a note on a requirement",
        "Only the author of a note (or a superuser) can change it.",
        parameters=[_path_id("note_pk", "ID of the note")],
        request=NoteSerializer,
        responses=_responses({200: NoteSerializer}),
    ),
    "notes_delete": _doc(
        "Delete a note from a requirement",
        "Only the author of a note (or a superuser) can delete it.",
        parameters=[_path_id("note_pk", "ID of the note")],
        responses=_responses({204: None}),
    ),
    "organisation": _doc(
        "Get the organisation linked to a requirement",
        responses=_responses({200: OrganisationLinkSerializer}),
    ),
    "organisation_create": _doc(
        "Link an organisation to a requirement",
        request=OrganisationLinkSerializer,
        responses=_responses({201: OrganisationLinkSerializer}),
    ),
    "organisation_delete": _doc(
        "Unlink the organisation from a requirement",
        responses=_responses({204: None}),
    ),
    "public_link": _doc(
        "List public links of a requirement",
        responses=_responses({200: PublicLinkSerializer(many=True)}, 403, 404),
    ),
    "public_link_create": _doc(
        "Create a public link for a requirement",
        "No request body - a new, active link is generated.",
        request=None,
        responses=_responses({201: PublicLinkSerializer}, 403, 404),
    ),
    "public_link_update": _doc(
        "Update a public link of a requirement",
        parameters=[
            OpenApiParameter(
                name="public_link_pk", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH,
                description="ID of the public link",
            )
        ],
        request=PublicLinkSerializer,
        responses=_responses({200: PublicLinkSerializer}),
    ),
    "public_link_delete": _doc(
        "Delete a public link of a requirement",
        parameters=[
            OpenApiParameter(
                name="public_link_pk", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH,
                description="ID of the public link",
            )
        ],
        responses=_responses({204: None}),
    ),
    "sprint": _doc(
        "List sprints of a requirement",
        responses=_responses({200: SprintSerializer(many=True)}, 403, 404),
    ),
    "sprint_create": _doc(
        "Create a sprint on a requirement",
        "`start_date` and `end_date` are required.",
        request=SprintSerializer,
        responses=_responses({201: SprintSerializer}),
    ),
    "sprint_delete": _doc(
        "Delete a sprint from a requirement",
        parameters=[_path_id("sprint_pk", "ID of the sprint")],
        responses=_responses({204: None}),
    ),
    "users_list_create": _doc(
        "Add a user to a requirement",
        request=UserListSerializer,
        responses=_responses({201: OpenApiResponse(description="User added")}),
    ),
    "users_list_delete": _doc(
        "Remove a user from a requirement",
        parameters=[_path_id("user_pk", "ID of the user")],
        responses=_responses({204: None}),
    ),
}
