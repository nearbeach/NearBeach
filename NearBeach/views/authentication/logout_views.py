"""Module providing the Authentication views for NearBeach"""
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View


class LogoutView(View):
    """Class handling authentication"""
    @staticmethod
    def get(request, *args, **kwargs):
        logout(request)

        return redirect("login")
