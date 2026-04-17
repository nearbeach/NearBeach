from NearBeach.models import (
    ObjectAssignment,
)


class LinkListService():
    """Service to help list/add/delete object links"""

    def __init__(self, destination: str, location_id: int):
        """Initialise the class"""
        self.destination = destination
        self.location_id = location_id

    def create_link(self, post_data):
        return

    def delete_link(self, link_pk):
        object_assignment_results = ObjectAssignment.objects.filter(
            is_deleted=False,
            pk=link_pk,
            **{self.destination: self.location_id},
        )

        # If there are no values to update - notify the user
        if len(object_assignment_results) == 0:
            return False

        # Soft delete the data
        object_assignment_results.update(is_deleted=True)

        return True

    def get_link_list(self):
        # TODO - fetch link data as formatted correctly
        # TODO - use serializer to format data
        return


