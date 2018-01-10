from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import  loader
from NearBeach.forms import *
from .models import *
from .namedtuplefetchall import *



@login_required(login_url='login')
def requirement_information(request, requirement_id):
    #Setup the initial data for the form
    requirement_results = requirements.objects.get(requirement_id=requirement_id)
    initial = {
        'requirement_title': requirement_results.requirement_title,
        'requirement_scope': requirement_results.requirement_scope,
        'requirement_type': requirement_results.requirement_type,
    }

    #Load template
    t = loader.get_template('NearBeach/requirement_information.html')

    # context
    c = {
        'requirement_id': requirement_id,
        'requirement_information_form': requirement_information_form(initial=initial),
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def requirement_items_edit(request, requirement_id):
    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_items_edit.html')

    # context
    c = {

    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def requirement_items_list(request, requirement_id):
    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_items_list.html')

    # context
    c = {

    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def requirement_items_new(request, requirement_id):
    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_items_new.html')

    # context
    c = {

    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def requirement_items_new_link(request, requirement_id):
    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_items_new_link.html')

    # context
    c = {

    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def requirement_items_list(request, requirement_id):
    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_items_list.html')

    # context
    c = {

    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def requirement_items_new_link(request, requirement_id):
    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_items_new_link.html')

    # context
    c = {

    }

    return HttpResponse(t.render(c, request))\



@login_required(login_url='login')
def requirement_links_list(request, requirement_id):
    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_links_list.html')

    # context
    c = {

    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def requirement_new_link(request, requirement_id):
    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_new_link.html')

    # context
    c = {

    }

    return HttpResponse(t.render(c, request))