import pytest
from django.utils.translation import trim_whitespace
from hypothesis import given, strategies as st
from hypothesis.extra.django import TestCase, from_model
from NearBeach.forms import OrganisationForm
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestOrganisationFormFuzzy(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    @given(
        organisation_name=st.text(min_size=1, max_size=100),
        organisation_website=st.text(min_size=1, max_size=100),
        organisation_email=st.emails(),
        change_user=from_model(User),
        creation_user=from_model(User),
    )
    def test_organisation_form_validation(
        self,
        organisation_name,
        organisation_website,
        organisation_email,
            change_user,
            creation_user,
    ):
        form_data = {
            "organisation_name": organisation_name,
            "organisation_website": organisation_website,
            "organisation_email": organisation_email,
        }
        form = OrganisationForm(data=form_data)

        # It should either be valid OR give meaningful errors
        if form.is_valid():
            # Create the organisation from the form
            organisation = form.save(commit=False)
            organisation.change_user = change_user
            organisation.creation_user = creation_user
            organisation.save()

            # Assert
            assert organisation.organisation_name == trim_whitespace(organisation_name)
            assert organisation.organisation_website == trim_whitespace(organisation_website)
            assert organisation.organisation_email == trim_whitespace(organisation_email)
        else:
            assert ("organisation_name" in form.errors
                    or "organisation_email" in form.errors
                    or "organisation_website" in form.errors
            )
