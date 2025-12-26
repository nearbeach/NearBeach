"""Module providing the Application views for NearBeach"""
from django.shortcuts import render
from django.views import View


class ApplicationView(View):
    """Class handing crud for ApplicationView"""
    def get(self, request, _ = None):
        return render(request, "NearBeach/Application.html")
