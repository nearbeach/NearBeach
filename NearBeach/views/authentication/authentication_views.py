"""Module providing the Authentication views for NearBeach"""

from django.shortcuts import render
from django.views import View
from drf_spectacular.utils import extend_schema


@extend_schema(exclude=True)
class AuthenticationView(View):
    """Class handling authentication"""

    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, "NearBeach/authentication/authentication.html")
