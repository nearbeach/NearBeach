"""Some placeholder view"""

from django.views.generic import TemplateView


class PlaceholderView(TemplateView):
    """Renders the placeholder page."""

    template_name = "NearBeach/placeholder.html"
