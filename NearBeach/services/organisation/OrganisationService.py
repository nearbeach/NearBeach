from django.db.models import Q, QuerySet
from rest_framework import status
from NearBeach.models.organisation import Organisation
from NearBeach.serializers.organisation_serializer import OrganisationSerializer

from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectServiceAbstraction,
    ServiceResponse,
)


class OrganisationService(ObjectServiceAbstraction):
    """Service to help create, read, update, and delete organisation objects and their associations"""
    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        serializer = OrganisationSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Save
        created_organisation = serializer.save(change_user=request.user)

        # Re-serialize
        serializer = OrganisationSerializer(created_organisation, many=False)

        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request: AuthenticatedRequest, _: None) -> ServiceResponse:
        organisation = Organisation.objects.filter(
            pk=self.location_id,
            is_deleted=False
        )
        if not organisation.exists():
            return "Organisation does not exist", status.HTTP_400_BAD_REQUEST

        organisation.update(
            is_deleted=True,
            change_user=request.user,
        )

        return {}, status.HTTP_204_NO_CONTENT

    # The view paginates the queryset itself (like the project list), so this returns the queryset rather than a
    # ServiceResponse. Organisations belong to no group, so everyone with organisation permission sees them all -
    # that permission is checked by the view.
    def get_list(self, request: AuthenticatedRequest) -> QuerySet[Organisation]:  # type: ignore[override]
        organisation_results = Organisation.objects.filter(
            is_deleted=False,
        ).order_by("name", "pk")

        # Filter by search parameter in the query string
        search = request.query_params.get("search", None)
        if search:
            organisation_results = organisation_results.filter(
                Q(name__icontains=search)
                | Q(email__icontains=search)
                | Q(website__icontains=search)
                | Q(id=int(search) if search.isdigit() else None)
            )

        return organisation_results

    def retrieve(self) -> ServiceResponse:
        organisation = Organisation.objects.filter(
            is_deleted=False,
            pk=self.location_id,
        ).first()

        if organisation is None:
            return "Organisation does not exist", status.HTTP_404_NOT_FOUND

        # Serialize the data
        serializer = OrganisationSerializer(
            organisation,
            many=False
        )

        return serializer.data, status.HTTP_200_OK

    def update(self, request: AuthenticatedRequest, _: None) -> ServiceResponse:
        organisation = Organisation.objects.filter(
            is_deleted=False,
            pk=self.location_id,
        ).first()
        if organisation is None:
            return "Organisation does not exist", status.HTTP_400_BAD_REQUEST

        serializer = OrganisationSerializer(
            organisation,
            data=request.data,
            partial=True,
            context={
                'request': request
            },
        )
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Update data
        updated_organisation = serializer.save(change_user=request.user)

        # Re-serialize the data to send back complete set to user
        serializer = OrganisationSerializer(updated_organisation, many=False)

        return serializer.data, status.HTTP_200_OK
