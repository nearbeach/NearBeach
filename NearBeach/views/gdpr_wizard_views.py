from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.template.loader import get_template
from NearBeach.views.theme_views import get_theme


@login_required(login_url="login", redirect_field_name="")
@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name="")
def gdpr_wizard(request):
    # Get template
    t = get_template("NearBeach/gdpr/gdpr_wizard.html")

    # Get context
    c = {
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))