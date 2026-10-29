from typing import Any

from rest_framework import viewsets, status
from django.db.models import F, QuerySet, Value
from rest_framework.response import Response
from NearBeach.api_docs import apply_schema
from NearBeach.api_docs.api_v1.potential_object_links_docs import POTENTIAL_OBJECT_LINKS_SCHEMA
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.models.project import Project
from NearBeach.models.requirement.requirement import Requirement
from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.models.task import Task
from NearBeach.models.user import UserGroup
from NearBeach.serializers.object_data.potential_object_link_serializer import PotentialObjectLinkSerializer


@apply_schema(POTENTIAL_OBJECT_LINKS_SCHEMA)
class PotentialObjectLinksViewSet(viewsets.ViewSet):
    """Class dealing for searching potential object links"""

    http_method_names = ["get"]

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.object_assignment_results: QuerySet[ObjectAssignment] = ObjectAssignment.objects.none()

    def _get_project(self):
        """Private method to get project object links"""
        results = (
            Project.objects.filter(
                is_deleted=False,
                id__in=self.object_assignment_results.filter(
                    project_id__isnull=False,
                ).values(
                    "project_id",
                ),
            )
            .annotate(
                object_id=F("id"),
                object_title=F("title"),
                object_type=Value("project"),
            )
            .values(
                "object_id",
                "object_title",
                "object_type",
            )
        )

        # Serialize the data
        serializer = PotentialObjectLinkSerializer(results, many=True)

        return serializer.data

    def _get_requirement(self):
        """Private method to get project object links"""
        results = (
            Requirement.objects.filter(
                is_deleted=False,
                id__in=self.object_assignment_results.filter(
                    requirement_id__isnull=False,
                ).values(
                    "requirement_id",
                ),
            )
            .annotate(
                object_id=F("id"),
                object_title=F("title"),
                object_type=Value("requirement"),
            )
            .values(
                "object_id",
                "object_title",
                "object_type",
            )
        )

        # Serialize the data
        serializer = PotentialObjectLinkSerializer(results, many=True)

        return serializer.data

    def _get_requirement_item(self):
        """Private method to get project object links"""
        results = (
            RequirementItem.objects.filter(
                is_deleted=False,
                id__in=self.object_assignment_results.filter(
                    requirement_item_id__isnull=False,
                ).values(
                    "requirement_item_id",
                ),
            )
            .annotate(
                object_id=F("id"),
                object_title=F("title"),
                object_type=Value("requirement_item"),
            )
            .values(
                "object_id",
                "object_title",
                "object_type",
            )
        )

        # Serialize the data
        serializer = PotentialObjectLinkSerializer(results, many=True)

        return serializer.data

    def _get_task(self):
        """Private method to get project object links"""
        results = (
            Task.objects.filter(
                is_deleted=False,
                id__in=self.object_assignment_results.filter(
                    task_id__isnull=False,
                ).values(
                    "task_id",
                ),
            )
            .annotate(
                object_id=F("id"),
                object_title=F("title"),
                object_type=Value("task"),
            )
            .values(
                "object_id",
                "object_title",
                "object_type",
            )
        )

        # Serialize the data
        serializer = PotentialObjectLinkSerializer(results, many=True)

        return serializer.data

    def list(self, request, *args, **kwargs):
        """Method used to fetch potential object links"""
        query_string = request.query_params.get("q")

        # Fetch objects the user has access too
        self.object_assignment_results = ObjectAssignment.objects.filter(
            is_deleted=False,
            group_id__in=UserGroup.objects.filter(
                is_deleted=False,
                username=request.user.id,
                group__isnull=False,
            ).values("group_id"),
        )

        # TODO - pass query string through
        # TODO - pass exclusion items through
        # TODO - limit results back
        # TODO - this the proper way with https://www.django-rest-framework.org/api-guide/filtering/
        # AKA Search Fields
        project_data = self._get_project()
        requirement_data = self._get_requirement()
        requirement_item_data = self._get_requirement_item()
        task_data = self._get_task()

        # Send back data
        return Response(
            project_data + requirement_data + requirement_item_data + task_data,
            status=status.HTTP_200_OK,
        )
