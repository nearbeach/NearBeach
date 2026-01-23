"""Module providing the Application views for NearBeach"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class ApplicationView(LoginRequiredMixin, View):
    """Class handing crud for ApplicationView"""
    login_url = "/login/"

    @staticmethod
    def get(request, _ = None):
        return render(request, "NearBeach/application.html")
