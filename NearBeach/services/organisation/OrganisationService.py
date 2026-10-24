from rest_framework import status
from NearBeach.decorators.check_user_permissions.destination_permission import destination_permission
from NearBeach.models.organisation import Organisation
from NearBeach.serializers.organisation_serializer import OrganisationSerializer

from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectId,
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

    def delete(self, request: AuthenticatedRequest, organisation_pk: ObjectId) -> ServiceResponse:
        organisation = Organisation.objects.get(pk=organisation_pk)
        organisation.is_deleted = True
        organisation.change_user = request.user
        organisation.save()

        return {}, status.HTTP_204_NO_CONTENT

    def get_data(self, _: AuthenticatedRequest) -> ServiceResponse:
        raise NotImplementedError  # Method not required in current class

    def get_list(self, request: AuthenticatedRequest) -> ServiceResponse:
        raise NotImplementedError  # Method not required in current class

    @destination_permission(min_permission_level=1)
    def list(self, _: AuthenticatedRequest) -> ServiceResponse:
        # TODO - Check how we are going to do serialization etc
        # TODO - paginate_queryset/get_paginated_response live on the viewset, not this service, and update()
        #  hands a queryset to serializer.update(). Neither works yet, but no view uses this class
        # Get the organisation results
        organisation_results = Organisation.objects.filter(
            is_deleted=False,
        )

        # Handle pagination
        page = self.paginate_queryset(organisation_results)  # type: ignore[attr-defined]
        if page is not None:
            serializer = OrganisationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)  # type: ignore[attr-defined]

        serializer = OrganisationSerializer(organisation_results, many=True)

        return serializer.data, status.HTTP_200_OK

    def update(self, request: AuthenticatedRequest, pk: ObjectId) -> ServiceResponse:
        serializer = OrganisationSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Double-check the organisation exists
        update_organisation = Organisation.objects.filter(
            is_deleted=False,
            pk=pk,
        )
        if len(update_organisation) == 0:
            return "Organisation does not exist", status.HTTP_400_BAD_REQUEST

        # Update data
        update_organisation.change_user = request.user  # type: ignore[attr-defined]
        update_organisation = serializer.update(
            update_organisation,
            serializer.data,
        )

        # Re-serialize the data to send back complete set to user
        serializer = OrganisationSerializer(
            update_organisation,
            many=False
        )

        return serializer.data, status.HTTP_200_OK
