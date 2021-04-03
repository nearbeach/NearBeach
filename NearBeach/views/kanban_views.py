from django.contrib.auth.decorators import login_required
from NearBeach.models import *
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.db.models import Sum, Q, Min
from NearBeach.forms import *
from NearBeach.views.tools.internal_functions import *
from NearBeach.user_permissions import return_user_permission_level
from django.db.models import Max

import json, urllib3


@login_required(login_url='login', redirect_field_name="")
@require_http_methods(['POST'])
def add_kanban_link(request,kanban_board_id,object_lookup):
    """

    :param request:
    :param destination:
    :param location_id:
    :return:
    """

    # CHECK USER PERMISSION LATER

    # Get form data and check
    form = AddKanbanLinkForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the newest card number id
    kanban_card_sort_number = get_max_sort_id(kanban_board_id, form)

    # Submit the kanban board link
    kanban_card_submit = kanban_card(
        change_user=request.user,
        kanban_board_id=kanban_board_id,
        kanban_column=form.cleaned_data['kanban_column'],
        kanban_level=form.cleaned_data['kanban_level'],
        kanban_card_sort_number=kanban_card_sort_number + 1,
    )

    # Check the data
    if object_lookup == 'project':
        kanban_card_submit.project = form.cleaned_data[object_lookup]
    elif object_lookup == 'task':
        kanban_card_submit.task = form.cleaned_data[object_lookup]
    elif object_lookup == 'requirement':
        kanban_card_submit.requirement = form.cleaned_data[object_lookup]

    kanban_card_submit.kanban_card_text = form.cleaned_data[object_lookup]

    # Save the data
    kanban_card_submit.save()

    # Send back the data we just created
    kanban_card_results = kanban_card.objects.get(kanban_card_id=kanban_card_submit.kanban_card_id)

    return HttpResponse(serializers.serialize('json',[kanban_card_results]),content_type='application/json')


@login_required(login_url='login', redirect_field_name="")
@require_http_methods(['POST'])
def check_kanban_board_name(request):
    """
    The following will get a list of all kanban boards with the same name. The idea is that each kanban board should
    have a unique name.
    :param request:
    :return:
    """

    # Get the form data
    form = CheckKanbanBoardName(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    kanban_board_results = kanban_board.objects.filter(
        is_deleted=False,
        kanban_board_name=form.cleaned_data['kanban_board_name'],
    )

    # Send back data
    return HttpResponse(serializers.serialize('json', kanban_board_results), content_type='application/json')


# Internal function
def get_max_sort_id(kanban_board_id,form):
    # Get the newest card number id
    kanban_card_sort_number = kanban_card.objects.filter(
        is_deleted=False,
        kanban_board_id=kanban_board_id,
        kanban_column=form.cleaned_data['kanban_column'],
        kanban_level=form.cleaned_data['kanban_level'],
    ).aggregate(Max('kanban_card_sort_number'))

    # If the card is new in that particular column & row - then we need to implement a sort number of 0
    if kanban_card_sort_number['kanban_card_sort_number__max'] == None:
        kanban_card_sort_number['kanban_card_sort_number__max'] = 0

    return kanban_card_sort_number['kanban_card_sort_number__max']


@login_required(login_url='login', redirect_field_name="")
def kanban_information(request, kanban_board_id):
    """

    :param request:
    :param kanban_board_id:
    :return:
    """

    # Check user's permissions

    # Get the kanban data
    kanban_board_results = kanban_board.objects.get(kanban_board_id=kanban_board_id)

    kanban_card_results = kanban_card.objects.filter(
        is_deleted=False,
        kanban_board_id=kanban_board_id,
    ).order_by('kanban_card_sort_number')

    column_results = kanban_column.objects.filter(
        is_deleted=False,
        kanban_board_id=kanban_board_id,
    )

    level_results = kanban_level.objects.filter(
        is_deleted=False,
        kanban_board_id=kanban_board_id,
    )

    # Get the template
    t = loader.get_template('NearBeach/kanban/kanban_information.html')

    # Context
    c = {
        'kanban_board_results': serializers.serialize('json', [kanban_board_results]),
        'kanban_card_results': serializers.serialize('json', kanban_card_results),
        'column_results': serializers.serialize('json', column_results),
        'kanban_board_id': kanban_board_id,
        'level_results': serializers.serialize('json', level_results),
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name="")
@require_http_methods(['POST'])
def kanban_link_list(request, kanban_board_id, object_lookup):
    """

    :param request:
    :param kanban_board_id:
    :return:
    """

    # CHECK USER PERMISSIONS

    # Get a list of all existing cards
    existing_objects = kanban_card.objects.filter(
        is_deleted=False,
        kanban_board_id=kanban_board_id,
    )

    # Get the results we require
    if object_lookup == "Project":
        object_results = project.objects.filter(
            is_deleted=False,
        ).exclude(project_id__in=existing_objects.exclude(
            project_id__isnull=True
        ).values('project_id'))
    elif object_lookup == "Requirement":
        object_results = requirement.objects.filter(
            is_deleted=False,
        ).exclude(requirement_id__in=existing_objects.exclude(
            requirement_id__isnull=True
        ).values('requirement_id'))
    elif object_lookup == "Task":
        object_results = task.objects.filter(
            is_deleted=False,
        ).exclude(task_id__in=existing_objects.exclude(
            task_id__isnull=True,
        ).values('task_id'))
    else:
        return HttpResponseBadRequest("Sorry - there was an issue with your object lookup")

    return HttpResponse(serializers.serialize('json', object_results), content_type='application/json')


@login_required(login_url='login', redirect_field_name="")
@require_http_methods(['POST'])
def move_kanban_card(request, kanban_card_id):
    """

    :param request:
    :param kanban_board_id:
    :return:
    """

    # CHECK USER PERMISSIONS

    # Get the kanban card instance
    kanban_card_update = kanban_card.objects.get(kanban_card_id=kanban_card_id)

    # Get the form data
    form = MoveKanbanCardForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Update the card data
    kanban_card_update.kanban_column = form.cleaned_data['new_card_column']
    kanban_card_update.kanban_level = form.cleaned_data['new_card_level']
    kanban_card_update.kanban_card_sort_number = form.cleaned_data['new_card_sort_number']
    kanban_card_update.save()

    """
    Update the sort order
    ~~~~~~~~~~~~~~~~~~~~~
    
    If both the old and new level/column destination are the same, we take the difference between the two values
    Otherwise we apply two sort orders to both the old and the new
    """
    if form.cleaned_data['new_card_column'] == form.cleaned_data['old_card_column'] and \
            form.cleaned_data['new_card_level'] == form.cleaned_data['old_card_level']:
        # The card has stayed in the same column/level
        resort_array = kanban_card.objects.filter(
            Q(
                Q(
                    is_deleted=False,
                    kanban_card_sort_number__range=[
                        form.cleaned_data['old_card_sort_number'],
                        form.cleaned_data['new_card_sort_number']
                    ],
                ) |
                Q(
                    is_deleted=False,
                    kanban_card_sort_number__range=[
                        form.cleaned_data['new_card_sort_number'],
                        form.cleaned_data['old_card_sort_number']
                    ],
                )
            ) &
            ~Q(
                kanban_card_id=kanban_card_id,
            )
        ).order_by('kanban_card_sort_number')

        # Determine if we are using a positive or negative delta - using math
        delta = (-1) * (form.cleaned_data['new_card_sort_number'] > form.cleaned_data['old_card_sort_number']) + \
                (form.cleaned_data['new_card_sort_number'] < form.cleaned_data['old_card_sort_number'])

        # Send the data away to get manipulated
        update_sort_number(resort_array, delta)
    else:
        """
        The cards have been moved outside the origianl column/level. We need to update both the old and new location's
        sort orders.
        
        The old location will have a delta -1, to move the higher cards into the place left by the card
        
        The new location will have a delta +1, to move the higher cards away, to create a space for the card
        """
        old_resort_array = kanban_card.objects.filter(
            Q(
                is_deleted=False,
                kanban_card_sort_number__gte=form.cleaned_data['old_card_sort_number'],
            ) &
            ~Q(
                kanban_card_id=kanban_card_id,
            )
        ).order_by('kanban_card_sort_number')

        new_resort_array = kanban_card.objects.filter(
            Q(
                is_deleted=False,
                kanban_card_sort_number__gte=form.cleaned_data['new_card_sort_number'],
            ) &
            ~Q(
                kanban_card_id=kanban_card_id,
            )
        ).order_by('kanban_card_sort_number')

        update_sort_number(old_resort_array, -1)
        update_sort_number(new_resort_array, 1)

    return HttpResponse("")


@login_required(login_url='login', redirect_field_name="")
def new_kanban(request):
    """

    :param request:
    :return:
    """

    # Check user permissions

    # Get data
    group_results = group.objects.filter(
        is_deleted=False,
    )

    # Get tempalte
    t = loader.get_template('NearBeach/kanban/new_kanban.html')

    # Context
    c = {
        'group_results': serializers.serialize('json', group_results),
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name="")
@require_http_methods(['POST'])
def new_kanban_card(request, kanban_board_id):
    """
    """

    # CHECK USER PERMISSIONS

    # Get the kanban instance
    kanban_instance = kanban_board.objects.get(kanban_board_id=kanban_board_id)

    # Get the form data
    form = NewKanbanCardForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the newest card number id
    kanban_card_sort_number = get_max_sort_id(kanban_board_id,form)

    # Save the data
    submit_kanban_card = kanban_card(
        change_user=request.user,
        kanban_board=kanban_instance,
        kanban_card_text=form.cleaned_data['kanban_card_text'],
        kanban_card_description=form.cleaned_data['kanban_card_description'],
        kanban_column=form.cleaned_data['kanban_column'],
        kanban_level=form.cleaned_data['kanban_level'],
        kanban_card_sort_number=kanban_card_sort_number + 1,
    )
    submit_kanban_card.save()

    # Send back the kanban card data
    kanban_card_results = kanban_card.objects.get(kanban_card_id=submit_kanban_card.kanban_card_id)
    return HttpResponse(serializers.serialize('json', [kanban_card_results]), content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def new_kanban_save(request):
    """

    :param request:
    :return:
    """

    # CHECK USERS PERMISSIONS

    # Check the user form
    form = NewKanbanForm(request.POST)
    if not form.is_valid():
        print(form.errors)
        return HttpResponseBadRequest(form.errors)

    # Create the kanban board
    submit_kanban_board = kanban_board(
        change_user=request.user,
        creation_user=request.user,
        kanban_board_name=form.cleaned_data['kanban_board_name'],
    )
    submit_kanban_board.save()

    # Get both lists
    column_title_list = request.POST.getlist("column_title")
    level_title_list = request.POST.getlist("level_title")

    # Loop through the column title list to save the titles
    for index, column_title in enumerate(column_title_list):
        submit_column_title = kanban_column(
            change_user=request.user,
            kanban_column_name=column_title,
            kanban_board=submit_kanban_board,
            kanban_column_sort_number=index,
        )
        submit_column_title.save()

    # Loop throuhg the level title list to save the titles
    for index, level_title in enumerate(level_title_list):
        submit_level_title = kanban_level(
            change_user=request.user,
            kanban_level_name=level_title,
            kanban_board=submit_kanban_board,
            kanban_level_sort_number=index,
        )
        submit_level_title.save()

    # Get the group list and apply the permissions
    group_list = request.POST.getlist("group_list")

    for single_group in group_list:
        # Get the group instance
        group_instance = group.objects.get(group_id=single_group)

        # Save the group instance against object assignment
        submit_object_assignment = object_assignment(
            group_id=group_instance,
            kanban_board=submit_kanban_board,
            change_user=request.user,
        )

        # Save
        submit_object_assignment.save()

    # Send back project_information URL
    return HttpResponse(reverse('kanban_information', args={submit_kanban_board.kanban_board_id}))


@login_required(login_url='login', redirect_field_name="")
@require_http_methods(['POST'])
def update_card(request):
    """
    The following function will update the card information sent through the form in POST
    """
    
    # ADD IN CHECKING USER PERMISSIONS

    # Get data and validate in the form
    form = KanbanCardForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data
    kanban_card_update = form.cleaned_data['kanban_card_id']
    kanban_card_update.kanban_card_text = form.cleaned_data['kanban_card_text']
    kanban_card_update.kanban_card_description = form.cleaned_data['kanban_card_description']
    kanban_card_update.save()

    return HttpResponse("")


# Internal Function
def update_sort_number(resort_array, delta):
    """
    The following function will loop through the resort array and apply the delta (which should be either a 1 or -1)
    :param resort_array:
    :param delta:
    :return:
    """
    for row in resort_array:
        row.kanban_card_sort_number = row.kanban_card_sort_number + delta
        row.save()
