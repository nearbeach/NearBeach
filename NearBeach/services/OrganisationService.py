from NearBeach.decorators.check_user_permissions.destination_permission import destination_permission
from NearBeach.models import (
    Organisation, Customer, ObjectAssignment
)
from NearBeach.serializers.organisation_link_serializer import OrganisationLinkSerializer
from NearBeach.serializers.organisation_serializer import OrganisationSerializer

from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction
from NearBeach.utils.dicts.object_dict import OBJECT_DICT


class OrganisationService(ObjectServiceAbstraction):
    """Service to help create, read, update, and delete organisation objects and their associations"""
    def create(self, request):
        serializer = OrganisationSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return serializer.errors, False

        # Save
        created_organisation = serializer.save(change_user=request.user)

        # Re-serialize
        serializer = OrganisationSerializer(created_organisation, many=False)

        return serializer, True

    def delete(self, request, organisation_pk: int):
        organisation = Organisation.objects.get(pk=organisation_pk)
        organisation.is_deleted = True
        organisation.change_user = request.user
        organisation.save()

        return True

    def get_data(self, _):
        """Method to extract out any organisation/customer data for a given destination / location"""
        # Get the object we wish to extract information for
        extract_object = OBJECT_DICT[self.destination].filter(
            is_deleted=False,
            pk=self.location_id,
        )

        # Check there is an object to extract information for
        if len(extract_object) == 0:
            return {"No object exists"}, False

        # Set up the initial return data
        organisations = Organisation.objects.filter(
            is_deleted=False,
            pk__in=extract_object.values('organisation_id'),
        )

        # TODO - figure out if we can use methods to extract data (and for it to be re-usable)
        data = {
            "id": None,
            "potential_organisations": Organisation.objects.filter(
                is_deleted=False,
            ).order_by(
                "name",
            ),
        }

        if len(organisations) > 0:
            # Get the organisation
            organisation = organisations.first()

            # Set the data attributes
            data['organisation'] = organisation
            data['customers'] = Customer.objects.filter(
                is_deleted=False,
                id__in=ObjectAssignment.objects.filter(
                    is_deleted=False,
                    customer_id__isnull=False,
                    **{F"{self.destination}_id": self.location_id},
                ).values("customer_id"),
            )
            data['potential_customers'] = Customer.objects.filter(
                is_deleted=False,
                organisation_id=organisation.pk,
            )

        # Serialize data
        serializer = OrganisationLinkSerializer(data)

        return serializer, True

    def get_list(self, request):
        pass

    def link_organisation(self, request):
        serializer = OrganisationLinkSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        # Get the object we wish to update
        update_object = OBJECT_DICT[self.destination].filter(
            is_deleted=False,
            pk=self.location_id,
        )

        # Check there is an object to update
        if len(update_object) == 0:
            return {"No object exists"}, False

        # Get organisation
        organisation_result = Organisation.objects.get(
            pk=serializer.validated_data["id"],
        )
        update_object.update(
            organisation=organisation_result,
        )

        # Send back data
        potential_customers = Customer.objects.filter(
            is_deleted=False,
            organisation_id=organisation_result.id,
        )

        # Serializer
        serializer = OrganisationLinkSerializer({
            "organisation": organisation_result,
            "potential_customers": potential_customers,
        })

        return serializer, True

    @destination_permission(min_permission_level=1)
    def list(self, _):
        # TODO - Check how we are going to do serialization etc
        # Get the organisation results
        organisation_results = Organisation.objects.filter(
            is_deleted=False,
        )

        # Handle pagination
        page = self.paginate_queryset(organisation_results)
        if page is not None:
            serializer = OrganisationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrganisationSerializer(organisation_results, many=True)

        return serializer

    def unlink_organisation(self):
        update_object = OBJECT_DICT[self.destination].filter(
            is_deleted=False,
            pk=self.location_id,
        )

        #Check there is an object to update
        if len(update_object) == 0:
            return {"No object exists"}, False

        # Remove organisation from object
        update_object.update(
            organisation=None,
        )

        return None, True

    def update(self, request, pk):
        serializer = OrganisationSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return serializer.errors, False

        # Double-check the organisation exists
        update_organisation = Organisation.objects.filter(
            is_deleted=False,
            pk=pk,
        )
        if len(update_organisation) == 0:
            return {"Organisation does not exist"}, False

        # Update data
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

        return serializer, True
