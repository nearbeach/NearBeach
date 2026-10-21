"""Module providing the private document views for NearBeach"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from NearBeach.models.document.document import Document
from NearBeach.models.user import UserGroup, UserProfilePicture
from NearBeach.models.document.document_permission import DocumentPermission
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.services.document.file_handler.HandleDocumentPermissions import FILE_HANDLER


class PrivateDocumentViews(LoginRequiredMixin, View):
    """Class handing crud for ApplicationView"""

    login_url = "/private/"

    @staticmethod
    def get(request, document_key, *args, **kwargs):
        """
        The following function will check;
        1. The user's permission to the document
        2. If the document exists

        From there it will use X-Sendfile to send the document.
        :param request:
        :param document_key:
        :return:
        """
        # Extract the user groups the user is associated with
        user_group_results = UserGroup.objects.filter(
            is_deleted=False,
            username=request.user,
        )

        # Extract the permissions the document is associated with
        document_permission_results = DocumentPermission.objects.filter(
            is_deleted=False,
            document__key=document_key,
        )

        # Consolidate at the object assignment
        object_assignment_results = ObjectAssignment.objects.filter(
            Q(
                is_deleted=False,
                # JOIN IN USER GROUPS
                group_id__in=user_group_results.values("group_id"),
            )
            & Q(
                Q(
                    # Kanban board
                    kanban_board__isnull=False,
                    kanban_board_id__in=document_permission_results.values("kanban_card__kanban_board_id"),
                )
                | Q(
                    # Project Links
                    project__isnull=False,
                    project_id__in=document_permission_results.values("project_id"),
                )
                | Q(
                    # Task links
                    task__isnull=False,
                    task_id__in=document_permission_results.values("task_id"),
                )
                | Q(
                    # Requirement
                    requirement__isnull=False,
                    requirement_id__in=document_permission_results.values("requirement_id"),
                )
                | Q(
                    # Requirement Item
                    # Have to use the requirement item's requirement as permissions are not on the item
                    requirement_id__in=RequirementItem.objects.filter(
                        is_deleted=False,
                        id__in=document_permission_results.values(
                            "requirement_item_id"
                        ),
                        id__isnull=False,
                    ).values("requirement_id")
                )
                | Q(
                    # Request for change
                    request_for_change__isnull=False,
                    request_for_change_id__in=document_permission_results.values(
                        "request_for_change_id"
                    ),
                )
            )
        )

        profile_picture_permission = document_permission_results.filter(
            Q(
                customer__isnull=False,
            )
            | Q(organisation__isnull=False)
        )

        new_object_picture = document_permission_results.filter(
            # If everything is empty, EXCEPT the UUID new object column
            new_object__isnull=False,
            project_id__isnull=True,
            request_for_change_id__isnull=True,
            requirement_id__isnull=True,
            requirement_item_id__isnull=True,
            task_id__isnull=True,
            kanban_card_id__isnull=True,
        )

        user_profile_picture = UserProfilePicture.objects.filter(
            document=document_key,
            is_deleted=False,
        )

        # If the object_assignment_results.count() == 0, then user does not have permissions
        if (
                object_assignment_results.count() == 0
                and profile_picture_permission.count() == 0
                and user_profile_picture.count() == 0
                and new_object_picture.count() == 0
                and request.user.is_superuser is False
        ):
            raise Http404

        # Get Document information
        document_results = get_object_or_404(Document, key=document_key)

        # If not a document but a URL
        if document_results.url_location:
            return HttpResponseRedirect(document_results.url_location)

        return FILE_HANDLER.fetch(document_results)
