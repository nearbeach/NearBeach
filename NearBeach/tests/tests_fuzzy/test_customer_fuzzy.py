from hypothesis import given, assume
from hypothesis.extra.django import TestCase, from_model, from_form
from hypothesis.strategies import lists

from NearBeach.forms import CustomerForm
from NearBeach.models import Customer, ListOfTitle, Organisation
from django.contrib.auth import get_user_model

User = get_user_model()


class TestOrganisationFuzzy(TestCase):
    @given(from_model(
        Customer,
        customer_title=from_model(
            ListOfTitle,
            change_user=from_model(User),
        ),
        change_user=from_model(User),
        organisation=from_model(
            Organisation,
            change_user=from_model(User),
        ),
    ))
    def test_is_customer_model(self, customer):
        self.assertIsInstance(customer, Customer)
        self.assertIsNotNone(customer.pk)

    # @given(from_model(
    #     Customer,
    #     change_user=from_model(User),
    #     organisation=from_model(
    #         Organisation,
    #         change_user=from_model(User),
    #     ),
    # ))
    # def test_can_get_multiple_models_with_unique_field(self, customer):
    #     assume(len(customer) > 1)
    #     for c in customer:
    #         self.assertIsNotNone(c.pk)
