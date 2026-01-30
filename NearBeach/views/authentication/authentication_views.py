"""Module providing the Authentication views for NearBeach"""
from django.shortcuts import render
from django.views import View


class AuthenticationView(View):
    """Class handling authentication"""
    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, "NearBeach/authentication/authentication.html")
