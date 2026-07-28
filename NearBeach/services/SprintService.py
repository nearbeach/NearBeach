from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction


class SprintService(ObjectServiceAbstraction):
    """Service to help create, read, update, delete sprint objects"""

    def create(self, request):
        pass

    def delete(self, request, sprint_id: int):
        pass

    def get_list(self, request):
        pass

    def update(self, request, sprint_id: int):
        pass
