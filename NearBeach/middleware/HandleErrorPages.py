from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.template.loader import get_template
from NearBeach.views.theme_views import get_theme


class TemplateErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Response
        response = self.get_response(request)

        if response.status_code == 404:
            # Get template
            template = get_template('404.html')

            # Context
            c = {
                "theme": get_theme(request),
            }

            response = HttpResponseNotFound(template.render(c))

        if response.status_code == 500:
            # Get template
            template = get_template('500.html')

            # Content
            c = {
                "theme": get_theme(request),
            }

            response = HttpResponseBadRequest(template.render(c))

        return response
