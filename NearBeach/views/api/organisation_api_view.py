from rest_framework.generics import get_object_or_404
from NearBeach.decorators.check_user_permissions.organisation_permissions import check_user_organisation_permissions
from NearBeach.models import (
    Customer,
    Organisation,
)
from NearBeach.serializers.organisation_serializer import OrganisationSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response

import datetime


class OrganisationViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = Organisation.objects.filter(is_deleted=False)
    serializer_class = OrganisationSerializer

    @check_user_organisation_permissions(min_permission_level=2)
    def create(self, request, *args, **kwargs):
        serializer = OrganisationSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create Organisation
        organisation_submit = Organisation(
            organisation_name=serializer.data.get("organisation_name"),
            organisation_website=serializer.data.get("organisation_website"),
            organisation_email=serializer.data.get("organisation_email"),
            change_user=request.user,
        )
        organisation_submit.save()

        return Response(
            data={"organisation_id": organisation_submit.organisation_id },
            status=status.HTTP_201_CREATED,
        )

    @check_user_organisation_permissions(min_permission_level=4)
    def destroy(self, request, pk=None, *args, **kwargs):
        organisation = Organisation.objects.get(pk=pk)
        organisation.is_deleted = True
        organisation.change_user = request.user
        organisation.save()
        return Response(data='organisation deleted')

    @check_user_organisation_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        # Setup Attributes
        page_size = int(request.query_params.get("page_size", 100))
        page_size = page_size if page_size <= 1000 else 1000
        page = int(request.query_params.get("page", 1))

        organisation_results = Organisation.objects.filter(
            is_deleted=False,
        )[(page - 1) * page_size : page * page_size]

        serializer = OrganisationSerializer(organisation_results, many=True)

        return Response(serializer.data)

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

    @check_user_organisation_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = OrganisationSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update Organisation
        update_organiation = Organisation.objects.get(pk=pk)
        update_organiation.organisation_name = serializer.data.get("organisation_name")
        update_organiation.organisation_website = serializer.data.get("organisation_website")
        update_organiation.organisation_email = serializer.data.get("organisation_email")
        update_organiation.date_modified = datetime.datetime.now()
        update_organiation.change_user = request.user

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
