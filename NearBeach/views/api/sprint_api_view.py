from django.db.models.fields import CharField, IntegerField, DateTimeField
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiExample
from NearBeach.decorators.check_user_permissions.api_sprint_permissions_v0 import check_api_sprint_permissions
from NearBeach.decorators.check_user_permissions.sprint_permissions import check_sprint_permission_with_sprint
from NearBeach.models import (
    ObjectAssignment,
    Sprint,
    SprintObjectAssignment,
    UserGroup,
)
from NearBeach.serializers.sprint_serializer import SprintSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q, Case, When, Value, F
from collections import namedtuple

from NearBeach.utils.objects.object_dictionary import ObjectDictionary
from NearBeach.utils.objects.object_status_dictionary import get_object_status_from_destination


@extend_schema(
    tags=["Sprint"]
)
class SprintViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = Sprint.objects.filter(is_deleted=False)
    serializer_class = SprintSerializer

    @staticmethod
    def _get_object_results(sprint_id):
        sprint_object_assignment_results = SprintObjectAssignment.objects.filter(
            is_deleted=False,
            sprint_id=sprint_id,
        )

        object_assignment_results = ObjectAssignment.objects.filter(
            Q(
                project_id__in=sprint_object_assignment_results.filter(project_id__isnull=False).values('project_id'),
                is_deleted=False,
                link_relationship="Subobject",
                parent_link="project",
            ) |
            Q(
                requirement_item_id__in=sprint_object_assignment_results.filter(requirement_item_id__isnull=False).values('requirement_item_id'),
                is_deleted=False,
                link_relationship="Subobject",
                parent_link="requirement_item",
            )
        )

        QueryStructure = namedtuple("QueryStructure", [
            "destination",
            "link_relationship",
            "parent_link",
            "exclude_parent_link",
        ])

        # Setup the variables
        results = []
        query_permutations = [
            QueryStructure("requirement_item", "", "", []),
            QueryStructure("project", "", "", ["requirement_item"]),
            QueryStructure("project", "Subobject", "requirement_item", []),
            QueryStructure("task", "", "", ["project", "requirement_item"]),
            QueryStructure("task", "Subobject", "requirement_item", []),
            QueryStructure("task", "Subobject", "project", []),
        ]
        
        for permutation in query_permutations:
            current_object = ObjectDictionary(permutation.destination)
            permutation_results = current_object.objects.filter(
                is_deleted=False,
                **{F"{permutation.destination}_id__in": sprint_object_assignment_results.filter(
                    **{F"{permutation.destination}_id__isnull": False}
                ).values(F"{permutation.destination}_id")},
                sprintobjectassignment__is_deleted=False,
            )
            
            # If there is a link relationship, apply it
            if not permutation.link_relationship == "":
                permutation_results = permutation_results.filter(
                    objectassignment__link_relationship=permutation.link_relationship,
                    objectassignment__is_deleted=False,
                    **{F"objectassignment__{permutation.parent_link}_id__in": sprint_object_assignment_results.filter(
                        **{F"{permutation.parent_link}_id__isnull": False}
                    ).values(F"{permutation.parent_link}_id")},
                )
            else:
                # When we have objects that are not linked, make sure we are filtering out any with links
                permutation_results = permutation_results.exclude(
                    **{F"{permutation.destination}_id__in": object_assignment_results.filter(
                        parent_link__in=permutation.exclude_parent_link,
                        **{F"{permutation.destination}_id__isnull": False},
                    ).values(F"{permutation.destination}_id")}
                )

            permutation_results = permutation_results.annotate(
                sprint_object_assignment_id=F("sprintobjectassignment__pk"),
                title=F(current_object.title),
                description=F(current_object.description),
                status_id=F(current_object.status),
                higher_order_status=F(current_object.higher_order_status),
                object_type=Value(permutation.destination),
                object_id=F(current_object.id),
            )

            if current_object.start_date is not None:
                permutation_results = permutation_results.annotate(
                    start_date=F(F"{permutation.destination}_start_date"),
                    end_date=F(F"{permutation.destination}_end_date"),
                )
            else:
                permutation_results = permutation_results.annotate(
                    start_date=Value(None, output_field=DateTimeField(null=True)),
                    end_date=Value(None, output_field=DateTimeField(null=True)),
                )


            if not permutation.link_relationship == "":
                permutation_results = permutation_results.annotate(
                    parent_object_type=Value(permutation.parent_link),
                    parent_object_id=F(F"objectassignment__{permutation.parent_link}_id"),
                )
            else:
                permutation_results = permutation_results.annotate(
                    parent_object_type=Value("", output_field=CharField(max_length=20,null=True)),
                    parent_object_id=Value(None, output_field=IntegerField(null=True)),
                )


            results.extend(
                permutation_results.values(
                    "sprint_object_assignment_id",
                    "title",
                    "description",
                    "status_id",
                    "higher_order_status",
                    "start_date",
                    "end_date",
                    "object_type",
                    "object_id",
                    "parent_object_type",
                    "parent_object_id",
                ).distinct()
           )

        return results

    @staticmethod
    def _get_status_results():
        # Get the status of the objects
        status_results = {}
        for destination in ["requirement_item", "project", "task"]:
            current_object = get_object_status_from_destination(destination)
            status_results[destination] = current_object.filter(
                is_deleted=False,
            ).annotate(
                value=F(F"{destination}_status_id"),
                label=F(F"{destination}_status"),
                higher_order_status=F(F"{destination}_higher_order_status"),
            ).values(
                "value",
                "label",
                "higher_order_status",
            )

        return status_results

    @extend_schema(
        description="""
# 📌 Description

Create Sprints to help manage projects/requirements.

# 🧾 Parameters

- Sprint Name: Name of the sprint
- Destination: The object the sprint will be connected too. Either Project or Destination.
- Location ID: The object's ID that the sprint will be connected to
- Sprint Start Date: Start date of the sprint
- Sprint End Date: End date of the sprint
        """,
        examples=[
            OpenApiExample(
                "Example 1",
                description="Create a new project",
                value={
                    "sprint_name": "Hello Sprint",
                    "destination": "project",
                    "location_id": 2,
                    "sprint_start_date": "2024-12-19 15:49:37",
                    "sprint_end_date": "2024-12-19 15:49:37",
                }
            )
        ],
    )
    @check_api_sprint_permissions(min_permission_level=3)
    def create(self, request, *args, **kwargs):
        serializer = SprintSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the sprint
        sprint_submit = serializer.save(
            change_user=request.user,
        )

        # Re-add the destination back for the serializer
        if sprint_submit.project is not None:
            sprint_submit.destination = "project"
            sprint_submit.location_id = sprint_submit.project_id

        if sprint_submit.requirement is not None:
            sprint_submit.destination = "requirement"
            sprint_submit.location_id = sprint_submit.requirement_id

        # Re-serialize the data
        serializer = SprintSerializer(
            sprint_submit,
            many=False,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        description="""
# 📌 Description

Delete sprints.


# ✅ Notes

Users will need to have the permission to delete.
        """
    )
    @check_sprint_permission_with_sprint(min_permission_level=4)
    def destroy(self, request, pk, *args, **kwargs):
        serializer = SprintSerializer(
            data=request.data,
            context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        delete_sprint = get_object_or_404(
            queryset=Sprint.objects.filter(
                is_deleted=False,
                **{F"{serializer.data.get('destination')}_id": serializer.data.get("location_id")},
            ),
            pk=pk,
        )

        delete_sprint.is_deleted=True
        delete_sprint.change_user=request.user
        delete_sprint.save()

        return Response(
            data='sprint deleted',
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        description="""
# 📌 Description

Lists all sprints within NearBeach.


# ✅ Notes

- Pagination is enabled on this list. Use `?Page=` to navigate to the appropriate page.
    """
    )
    def list(self, request, *args, **kwargs):
        object_assignment_results = ObjectAssignment.objects.filter(
            is_deleted=False,
            group_id__in=UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            ).values(
                "group_id",
            )
        )

        sprint_results = Sprint.objects.filter(
            Q(
                is_deleted=False,
                project_id__in=object_assignment_results.filter(
                    project_id__isnull=False,
                ).values(
                    "project_id"
                ),
            ) |
            Q(
                is_deleted=False,
                requirement_id__in=object_assignment_results.filter(
                    requirement_id__isnull=False,
                ).values(
                    "requirement_id"
                ),
            )
        ).annotate(
            destination=Case(
                When(project_id__isnull=False, then=Value("project")),
                When(requirement_id__isnull=False, then=Value("requirement")),
                default=Value("")
            ),
            location_id=Case(
                When(project_id__isnull=False, then=F("project_id")),
                When(requirement_id__isnull=False, then=F("requirement_id")),
                default=Value(0)
            )
        )

        # Handle pagination
        page = self.paginate_queryset(sprint_results)
        if page is not None:
            serializer = SprintSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SprintSerializer(sprint_results, many=True)

        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Retrieves a single sprint.

    """
    )
    @check_sprint_permission_with_sprint(min_permission_level=1)
    def retrieve(self, request, pk, *args, **kwargs):
        queryset = Sprint.objects.all()
        sprint_results = get_object_or_404(
            queryset,
            pk=pk
        )

        if sprint_results.project is not None:
            sprint_results.destination = "project"
            sprint_results.location_id = sprint_results.project_id

        if sprint_results.requirement is not None:
            sprint_results.destination = "requirement"
            sprint_results.location_id = sprint_results.requirement_id

        sprint_results.status_results = self._get_status_results()
        sprint_results.object_results = self._get_object_results(pk)

        serializer = SprintSerializer(sprint_results)
        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Updates a single sprint.

# 🧾 Parameters

- Sprint Name: Name of the sprint
- Destination: The object the sprint will be connected too. Either Project or Destination.
- Location ID: The object's ID that the sprint will be connected to
- Sprint Start Date: Start date of the sprint
- Sprint End Date: End date of the sprint
    """
    )
    @check_sprint_permission_with_sprint(min_permission_level=2)
    def update(self, request, pk, *args, **kwargs):
        serializer = SprintSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        update_sprint = get_object_or_404(
            queryset=Sprint.objects.filter(
                is_deleted=False,
                **{F"{serializer.data.get('destination')}_id": serializer.data.get("location_id")},
            ),
            pk=pk,
        )
        
        # Update sprint
        update_sprint = serializer.update(update_sprint, serializer.validated_data)

        # Re-serialize the sprint data
        update_sprint.destination = serializer.data.get("destination")
        update_sprint.location_id = serializer.data.get("location_id")
        serializer = SprintSerializer(update_sprint)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
