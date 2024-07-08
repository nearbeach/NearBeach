from django.http import HttpResponse
from django.template.loader import get_template, TemplateDoesNotExist
from django.conf import settings
from NearBeach.views.theme_views import get_theme



class TemplateErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Response
        response = self.get_response(request)

        # On debug send back response
        if settings.DEBUG:
            return response

        try:
            # Error Template
            t = get_template(f"{response.status_code}.html")

            # Context
            c = {
                "nearbeach_title": "error",
                "need_tinymce": False,
                "theme": get_theme(request),
            }

            # Return
            response = HttpResponse(
                t.render(c, request),
                status=response.status_code,
            )
        except TemplateDoesNotExist:
            pass
        return response

