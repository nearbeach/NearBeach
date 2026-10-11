"""Regression tests for creator attribution during project creation."""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITransactionTestCase

from NearBeach.models import (
    Group,
    ListOfProjectStatus,
    ObjectAssignment,
    PermissionSet,
    Project,
    UserGroup,
)
from NearBeach.utils.enums.permission_enums import PermissionLevel


class ProjectCreationTests(APITransactionTestCase):
    # Run requests without the outer transaction used by APITestCase.
    # This allows database constraint errors to surface during the request.

    def setUp(self):
        user_model = get_user_model()

        self.assertFalse(
            user_model.objects.filter(pk=1).exists(),
            "This reproduction requires no pre-existing user with ID 1.",
        )

        self.user = user_model.objects.create_user(
            pk=100,
            username="project_creator",
            password=None,
        )

        audit_fields = {
            "creation_user": self.user,
            "change_user": self.user,
        }

        self.group = Group.objects.create(
            name="Project team",
            **audit_fields,
        )

        permissions = PermissionSet.objects.create(
            name="Project creator",
            project=PermissionLevel.ADD_AND_EDIT,
            **audit_fields,
        )

        UserGroup.objects.create(
            username=self.user,
            group=self.group,
            permission_set=permissions,
            **audit_fields,
        )

        # Transactional cleanup removes migration-created data between tests.
        # Ensure project creation has an available status in every test.
        if not ListOfProjectStatus.objects.filter(is_deleted=False).exists():
            ListOfProjectStatus.objects.create(
                status="New",
                sort_order=0,
                **audit_fields,
            )

        self.client.force_login(self.user)

    def assert_project_creation(self):
        response = self.client.post(
            "/api/v1/project/",
            {
                "title": "API regression project",
                "group_list": [self.group.pk],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            response.content.decode(),
        )

        project = Project.objects.get(pk=response.data["id"])
        self.assertEqual(project.creation_user_id, self.user.pk)

        assignment = ObjectAssignment.objects.get(
            project=project,
            group=self.group,
        )
        self.assertEqual(assignment.creation_user_id, self.user.pk)
        self.assertEqual(assignment.change_user_id, self.user.pk)

    def test_create_project_without_user_one(self):
        """Project creation does not depend on user ID 1."""
        self.assert_project_creation()

    def test_create_project_with_unrelated_user_one(self):
        """The assignment creator is the requesting user, not user ID 1."""
        get_user_model().objects.create_user(
            pk=1,
            username="unrelated_user",
            password=None,
        )

        self.assert_project_creation()