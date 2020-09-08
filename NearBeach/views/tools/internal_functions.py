from NearBeach.models import *

# Internal function
def get_object_from_destination(input_object,destination,location_id):
    """
    To stop the repeat code of finding specific objects using destination and location_id - we will import
    the object filter for it here - before returning it.
    :param object: The object we want to filter
    :param destination: The destination we are interested in
    :param location_id: The location_id
    :return:
    """
    if destination == "requirement":
        input_object = input_object.filter(
            requirement_id=location_id,
        )
    elif destination == "project":
        input_object = input_object.filter(
            project_id=location_id,
        )
    elif destination == "task":
        input_object = input_object.filter(
            task_id=location_id,
        )

    # Just send back the array
    return input_object


# Internal function
def set_object_from_destination(input_object,destination,location_id):
    """
    This function is used to set data against an object using the destination and location data.
    :param input_object: The input object that we are setting data for
    :param destination: The destination we are interested in
    :param location_id: The location we are interested in
    :return:
    """
    if destination == "project":
        input_object.project = project.objects.get(project_id=location_id)
    elif destination == "task":
        input_object.task = task.objects.get(task_id=location_id)
    elif destination == "requirement":
        input_object.requirement = requirement.objects.get(requirement_id=location_id)

    # Return what we have
    return input_object