from NearBeach.models import (
    Customer, ObjectAssignment
)
from NearBeach.serializers.customer_link_serializer import CustomerLinkSerializer
from NearBeach.serializers.customer_serializer import CustomerSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction


class CustomerService(ObjectServiceAbstraction):
    """Service to help create, read, update, and delete customer objects and their associations"""

    def _get_list(self):
        # Send back data to user
        customer_results = Customer.objects.filter(
            id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                customer_id__isnull=False,
                **{F"{self.destination}_id": self.location_id},
            ).values("customer_id"),
        )

        serializer = CustomerSerializer(customer_results)

        return serializer


    def create(self, request):
        serializer = CustomerSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        customer_submit = serializer.save(
            change_user=request.user,
        )

        serializer = CustomerSerializer(customer_submit)

        return serializer, True

    def delete(self, request, customer_pk: int):
        customer = Customer.objects.get(pk=customer_pk)
        customer.is_deleted = True
        customer.change_user = request.user
        customer.save()

        return True

    def get_list(self, request):
        return self._get_list()

    def link_customer(self, request):
        serializer = CustomerLinkSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        # Add customer to object
        submit_object_assignment = ObjectAssignment(
            customer_id=serializer.validated_data['id'],
            change_user=request.user,
            **{F"{self.destination}_id": self.location_id},
        )

        # Save the data
        submit_object_assignment.save()

        # Send back data to user
        serializer = self._get_list()

        return serializer, True

    def unlink_customer(self, customer_id):
        # Get the object link
        object_assignment_results = ObjectAssignment.objects.filter(
            customer_id=customer_id,
            is_deleted=False,
            **{F"{self.destination}_id": self.location_id},
        )

        if len(object_assignment_results) == 0:
            return {"Can not find customer/object connection"}, False

        # Update the results
        object_assignment_results.update(
            is_deleted=True,
        )

        # Send data back to user
        serializer = self._get_list()

        return serializer, True

    def update(self, request, pk):
        serializer = CustomerSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        # TODO - check how we want to use serializers to update objects
        # TODO - check to see if we want to do partial updates
        # Update serializer
        serializer.change_user = request.user
        serializer.save()

        return serializer, True
