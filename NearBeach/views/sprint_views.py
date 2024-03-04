from django.http.response import HttpResponse, HttpResponseBadRequest
from django.template import loader

def delete_sprint(request, sprint_id):
    return HttpResponse("")


def list_sprints(request, destination, location_id):
    return HttpResponse("")


def new_sprint(request, destination, location_id):
    return HttpResponse("")


def sprint_information(request, sprint_id):
    # Get the template
    t = loader.get_template("NearBeach/sprints/sprint_information.html")

    c = {}

    return HttpResponse(t.render(c, request))


def sprint_information_save(request, sprint_id):
    return HttpResponse("")


