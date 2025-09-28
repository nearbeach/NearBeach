from hypothesis import given, assume
from hypothesis.extra.django import TestCase, from_model, from_form
from hypothesis.strategies import lists

from NearBeach.models import Organisation
from django.contrib.auth import get_user_model

User = get_user_model()


class TestOrganisationModelFuzzy(TestCase):
    @given(from_model(
        Organisation,
        change_user=from_model(User),
    ))
    def test_is_organisation(self, organisation):
        self.assertIsInstance(organisation, Organisation)
        self.assertIsNotNone(organisation.pk)
        
    @given(lists(from_model(
        Organisation,
        change_user=from_model(User),
    )))
    def test_can_get_multiple_models_with_unique_field(self, organisations):
        assume(len(organisations) > 1)
        for c in organisations:
            self.assertIsNotNone(c.pk)
