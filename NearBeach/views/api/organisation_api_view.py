from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.generics import get_object_or_404
from NearBeach.decorators.check_user_permissions.organisation_permissions import check_user_organisation_permissions
from NearBeach.models import (
    Customer,
    Organisation,
)
from NearBeach.serializers.organisation_serializer import OrganisationSerializer
from NearBeach.serializers.organiation_list_serializer import OrganisationListSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response

import datetime


@extend_schema(
    tags=["Organisation"]
)
class OrganisationViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = Organisation.objects.filter(is_deleted=False)
    serializer_class = OrganisationSerializer
    http_method_names = ["get", "post", "put", "delete"]

    @extend_schema(
        description="""
# 📌 Description

Create Organisations.

# 🧾 Parameters

- Organisation Name: Name of the organisation
- Organisation Email: A generic email for the organisation. Tip you can use noreply@organisation.com
- Organisation Website: The website of the organisation

        """,
        examples=[
            OpenApiExample(
                "Example 1",
                description="Create a new organisation",
                value={
                    "organisation_name": "API Organisation",
                    "organisation_website": "https://nearbeach.org",
                    "organisation_email": "noreply@nearbeahc.org",
                }
            )
        ],
    )
    @check_user_organisation_permissions(min_permission_level=2)
    def create(self, request, *args, **kwargs):
        serializer = OrganisationSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save
        created_organisation = serializer.save(change_user=request.user)

        # Re-serialize
        serializer = OrganisationSerializer(created_organisation, many=False)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        description="""
# 📌 Description

Delete organisations.


# ✅ Notes

Users will need to have the permission to delete.
        """
    )
    @check_user_organisation_permissions(min_permission_level=4)
    def destroy(self, request, pk=None, *args, **kwargs):
        organisation = Organisation.objects.get(pk=pk)
        organisation.is_deleted = True
        organisation.change_user = request.user
        organisation.save()
        return Response(
            data='organisation deleted',
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        description="""
# 📌 Description

Lists all organisations within NearBeach.


# ✅ Notes

- Pagination is enabled on this list. Use `?page=` to navigate to the appropriate page.
    """
    )
    @check_user_organisation_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        # Get the organisation results
        organisation_results = Organisation.objects.filter(
            is_deleted=False,
        )

        # Handle pagination
        page = self.paginate_queryset(organisation_results)
        if page is not None:
            serializer = OrganisationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrganisationListSerializer(organisation_results, many=True)

        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Retrieves a single organisation.

    """
    )
    @check_user_organisation_permissions(min_permission_level=1)
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Organisation.objects.all()
        organisation_results = get_object_or_404(
            queryset,
            pk=pk
        )

        # Add customers
        organisation_results.customers = Customer.objects.filter(
            is_deleted=False,
            organisation_id=pk,
        )

        serializer = OrganisationSerializer(organisation_results)
        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Updates a single organisation.

# 🧾 Parameters

- Organisation Name: Name of the organisation
- Organisation Email: A generic email for the organisation. Tip you can use noreply@organisation.com
- Organisation Website: The website of the organisation

    """
    )
    @check_user_organisation_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = OrganisationSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Double check the organisation exists
        queryset = Organisation.objects.filter(
            is_deleted=False,
        )
        update_organisation = get_object_or_404(
            queryset,
            pk=pk,
        )
        update_organisation.change_user = request.user
        update_organisation = serializer.update(
            update_organisation,
            serializer.data,
        )

        # Re-serialize the data to send back complete set to user
        serializer = OrganisationSerializer(
            update_organisation,
            many=False
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
