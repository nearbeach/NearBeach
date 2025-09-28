from hypothesis import given, strategies as st
from hypothesis.extra.django import TestCase, from_model
from django.contrib.auth import get_user_model
from django.urls import reverse
import pytest
from rest_framework.test import APIClient

from NearBeach.models import ListOfTitle

User = get_user_model()

class TestCustomerApiFuzzy(TestCase):
    fixtures = ['NearBeach_basic_setup.json']
    data_dict = {}
    
    """
    {
      "customer_title": "2",
      "customer_first_name": "Socks",
      "customer_last_name": "Fluffy",
      "customer_email": "socks@nearbeahc.org"
    }
    """
    @given(
        change_user=from_model(User),
        customer_title=from_model(
            ListOfTitle,
            change_user=from_model(User),
        ),
        customer_first_name=st.text(min_size=1, max_size=50),
        customer_last_name=st.text(min_size=1, max_size=50),
        customer_email=st.emails()
    )
    def test_customer_api_post_authenticated(self, customer_name, customer_email):
        user = User.objects.get(pk=1)
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post(
            "/api/customers/",
            {
                "customer_name": customer_name,
                "customer_email": customer_email,
            },
            format="json"
        )

        assert response.status_code in (201, 400)
