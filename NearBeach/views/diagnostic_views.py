import json

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.views.decorators.http import require_http_methods

from NearBeach.forms import DiagnosticUploadTestForm
from NearBeach.views.document_views import handle_document_permissions
from NearBeach.views.theme_views import get_theme


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name="")
def diagnostic_email_test(request):
    try:
        default_email = getattr(settings, "DEFAULT_FROM_EMAIL", "error@error.com")

        send_mail(
            "NearBeach Diagnostic Test Email. EOM",
            "Please ignore.",
            default_email,
            [request.user.email],
            fail_silently=False,
        )

        return HttpResponse("")
    except Exception as e:
        return HttpResponseBadRequest(F"Could not send email test. Error -> {e}")


@login_required(login_url="login", redirect_field_name="")
@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name="")
def diagnostic_information(request):
    """

    """
    t = loader.get_template("./NearBeach/diagnostics/diagnostic_information.html")

    allowed_hosts = settings.ALLOWED_HOSTS
    csrf_trusted_urls = getattr(settings, "CSRF_TRUSTED_URLS", [])

    # Try and get the attributes, with a default of "". If it is "" means it has not been setup correctly.
    smtp_email_host = not getattr(settings, "EMAIL_HOST", None) is None
    smtp_email_host_user = not getattr(settings, "EMAIL_HOST_USER", None) is None

    c = {
        "allowed_hosts": allowed_hosts,
        "aws_access_key_id": F"{hasattr(settings, 'AWS_ACCESS_KEY_ID')}".lower(),
        "aws_secret_access_key": F"{hasattr(settings, 'AWS_SECRET_ACCESS_KEY')}".lower(),
        "aws_s3_endpoint_url": F"{hasattr(settings, 'AWS_S3_ENDPOINT_URL')}".lower(),
        "aws_storage_bucket_name": F"{hasattr(settings, 'AWS_STORAGE_BUCKET_NAME')}".lower(),
        "azure_storage_connection_string": F"{hasattr(settings, 'AZURE_STORAGE_CONNECTION_STRING')}".lower(),
        "azure_storage_container_name": F"{hasattr(settings, 'AZURE_STORAGE_CONTAINER_NAME')}".lower(),
        "csrf_trusted_urls": csrf_trusted_urls,
        "nearbeach_title": "Diagnostic Information",
        "smtp_email_host": F"{smtp_email_host}".lower(),
        "smtp_email_host_user": F"{smtp_email_host_user}".lower(),
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name="")
def diagnostic_upload_test(request):
    # Get the form data
    form = DiagnosticUploadTestForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Submit the form
    file = form.cleaned_data["document"]
    document_description = str(file)

    try:
        # Upload the document
        _, document_results = handle_document_permissions(
            request,
            request.FILES["document"],
            file,
            document_description,
            "new_object",
            form.cleaned_data["uuid"],
            0,
        )
    except ValueError:
        a = "hello world"
        return HttpResponseBadRequest(ValueError)


    # Send back json data
    json_results = json.dumps(list(document_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type="application/json")
