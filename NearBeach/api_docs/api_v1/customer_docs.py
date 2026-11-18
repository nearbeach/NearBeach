"""Swagger/OpenAPI documentation for CustomerViewSet.

Kept apart from the controller so the view stays thin. The view applies it with
`@extend_schema_view(**CUSTOMER_SCHEMA)` - keys are the view's method names.

The sub-endpoints (notes, groups, ...) build their `Response` by hand, so drf-spectacular can not
work out what they return - every one is described here with `request=` / `responses=`.
"""
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, OpenApiTypes, extend_schema

from NearBeach.serializers.customer_serializer import (
    CustomerSerializer,
)

TAGS = ["Customer"]

# Errors shared by the endpoints. 403 covers "not logged in" as well as "no permission".
_ERRORS = {
    400: OpenApiResponse(description="Invalid input - field errors, or a message such as 'Object does not exist'"),
    403: OpenApiResponse(description="Not logged in, or no permission for this customer"),
    404: OpenApiResponse(description="Customer not found"),
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


CUSTOMER_SCHEMA = {
    "list": _doc(
        "List customers",
        "Paginated list of customers the user can see. Filter with `?search=` (title or id).",
        responses={
            **_responses({200: CustomerSerializer(many=True)}, 403),
            404: OpenApiResponse(description="Invalid page number"),
        },
    ),
    "create": _doc(
        "Create a customer",
        "Requires permission level 3 or above. `group_list` is required and must only contain groups "
        "the user belongs to.",
        responses=_responses({201: CustomerSerializer}, 400, 403),
    ),
    "retrieve": _doc("Get a customer", responses=_responses({200: CustomerSerializer}, 403, 404)),
    "partial_update": _doc(
        "Update a customer",
        "Send only the fields to change. `meta_data` is merged into the stored JSON object (JSON Merge "
        "Patch): keys you send are added or updated, keys you leave out are kept, and a key set to `null` "
        "is deleted. It must be an object and the saved result is limited to 64KB.",
        request=CustomerSerializer,
        responses=_responses({200: CustomerSerializer}, 400, 403, 404),
    ),
    "destroy": _doc(
        "Delete a customer",
        "Soft-deletes the customer. Requires full permission (level 4).",
        responses=_responses({204: None}, 403, 404),
    ),
}
