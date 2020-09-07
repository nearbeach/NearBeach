
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.template import loader

from ..forms import *

@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def document_upload(request,destination,location_id,folder_id):
    """
    The following function will deal with the uploaded document. It will first;
    1. Check user's permission
    2. Place the request.POST values into a form for validation
    3. Create a new row in document and store the relevant data inside
    4. Create a new row in document permission and assign it to the appropriate object
    5. Send back the document information in JSON format
    :param request:
    :param destination: the object in question
    :param location_id: The location of the object
    :param folder_id: Which folder we will associate this with
    :return:
    """

    # WRITE CODE TO CHECK THE USER'S PERMISSION

    form = DocumentUploadForm(request.POST,request.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Create a new row for documentation

    return HttpResponse("HELLO WORLD - I have to complete this tomorrow")