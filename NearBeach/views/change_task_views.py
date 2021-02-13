from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from NearBeach.forms import ChangeTaskStatusForm
from NearBeach.models import change_task


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def update_status(request,change_task_id):
    """

    :param request:
    :param change_task_id:
    :return:
    """

    # Get form data
    form = ChangeTaskStatusForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get change task
    change_task_results = change_task.objects.get(change_task_id=change_task_id)

    # Update the change task results
    change_task_results.change_task_status = form.cleaned_data['change_task_status']
    change_task_results.save()

    return HttpResponse("")
