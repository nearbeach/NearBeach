from NearBeach.models import kanban_board, kanban_card, opportunity, organisation, quote, project, request_for_change, requirement, requirement_item, task, whiteboard


# Internal function
def get_object_from_destination(input_object, destination, location_id):
    """
    To stop the repeat code of finding specific objects using destination and location_id - we will import
    the object filter for it here - before returning it.
    :param object: The object we want to filter
    :param destination: The destination we are interested in
    :param location_id: The location_id
    :return:
    """
    if destination == "kanban_board":
        input_object = input_object.filter(
            kanban_board_id=location_id,
        )
    if destination == "kanban_card":
        input_object = input_object.filter(
            kanban_card_id=location_id,
        )
    elif destination == "opportunity":
        input_object = input_object.filter(
            opportunity_id=location_id,
        )
    elif destination == "organisation":
        input_object = input_object.filter(
            organisation_id=location_id,
        )
    elif destination == "project":
        input_object = input_object.filter(
            project_id=location_id,
        )
    elif destination == "quote":
        input_object = input_object.filter(
            quote_id=location_id,
        )
    elif destination == "requirement":
        input_object = input_object.filter(
            requirement_id=location_id,
        )
    elif destination == "request_for_change":
        input_object = input_object.filter(
            request_for_change_id=location_id,
        )
    elif destination == "requirement_item":
        input_object = input_object.filter(
            requirement_item_id=location_id,
        )
    elif destination == "task":
        input_object = input_object.filter(
            task_id=location_id,
        )
    elif destination == "whiteboard":
        input_object = input_object.filter(
            whiteboard_id=location_id,
        )

    # Just send back the array
    return input_object


# Internal function
def set_object_from_destination(input_object, destination, location_id):
    """
    This function is used to set data against an object using the destination and location data.
    :param input_object: The input object that we are setting data for
    :param destination: The destination we are interested in
    :param location_id: The location we are interested in
    :return:
    """
    if destination == "kanban_board":
        input_object.kanban_board = kanban_board.objects.get(kanban_board_id=location_id)
    if destination == "kanban_card":
        input_object.kanban_card = kanban_card.objects.get(kanban_card_id=location_id)
    elif destination == "opportunity":
        input_object.opportunity = opportunity.objects.get(object_id=location_id)
    elif destination == "organisation":
        input_object.organisation = organisation.objects.get(organisation_id=location_id)
    elif destination == "quote":
        input_object.quote = quote.objects.get(quote_id=location_id)
    if destination == "project":
        input_object.project = project.objects.get(project_id=location_id)
    elif destination == "request_for_change":
        input_object.request_for_change = request_for_change.objects.get(request_for_change_id=location_id)
    elif destination == "requirement":
        input_object.requirement = requirement.objects.get(requirement_id=location_id)
    elif destination == "requirement_item":
        input_object.requirement_item = requirement_item.objects.get(requirement_item_id=location_id)
    elif destination == "task":
        input_object.task = task.objects.get(task_id=location_id)
    elif destination == "whiteboard":
        input_object.whiteboard = whiteboard.objects.get(white_board_id=location_id)

    # Return what we have
    return input_object
