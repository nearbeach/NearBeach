"""Module providing the public link views for NearBeach"""

from django.shortcuts import render, redirect
from django.views import View

from NearBeach.models.misc.misc import PublicLink


class PublicLinkView(View):
    """Class handing crud for ApplicationView"""

    @staticmethod
    def get(request, public_link_id, *args, **kwargs):
        # Check to make sure object exists
        public_link_results = PublicLink.objects.filter(
            is_deleted=False,
            is_active=True,
            id=public_link_id,
        )

        # If there are no matching public links, redirect to the login page
        if len(public_link_results) == 0:
            return redirect('login')

        return render(request, "NearBeach/public_link/public_link.html")
