"""Extra rows for the requirement and requirement item permission tests.

NearBeach_basic_setup.json has notes, public links, sprints and links for requirements 1 and 2, but no folders or
documents at all (and no links for requirement items). The permission tests need them, so they are created here with
fixed ids that the test files refer to. Requirement 1 / item 1 are in the Administration group, requirement 2 /
item 2 are in the QA Team - the same split as projects 1 and 2.
"""
from django.contrib.auth import get_user_model

from NearBeach.models.document.document import Document
from NearBeach.models.document.document_permission import DocumentPermission
from NearBeach.models.document.folder import Folder
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment

# Folders
REQUIREMENT_1_FOLDER = 1001
REQUIREMENT_2_FOLDER = 1002
ITEM_1_FOLDER = 2001
ITEM_2_FOLDER = 2002

# Documents - a link and an uploaded file for each object
REQUIREMENT_1_LINK = "00000000-aaaa-4000-8000-000000000001"
REQUIREMENT_1_FILE = "00000000-aaaa-4000-8000-000000000002"
REQUIREMENT_2_FILE = "00000000-aaaa-4000-8000-000000000003"
REQUIREMENT_2_LINK = "00000000-aaaa-4000-8000-000000000004"
ITEM_1_LINK = "00000000-bbbb-4000-8000-000000000001"
ITEM_1_FILE = "00000000-bbbb-4000-8000-000000000002"
ITEM_2_FILE = "00000000-bbbb-4000-8000-000000000003"
ITEM_2_LINK = "00000000-bbbb-4000-8000-000000000004"

# Links of requirement items (object assignments)
ITEM_1_LINK_ROW = 9001
ITEM_2_LINK_ROW = 9002
ITEM_2_OTHER_LINK_ROW = 9003


class RequirementRelatedFixtures:
    """Mixin for BaseApiClass - put it first in the bases so its setUp runs after the base class has logged in"""

    def setUp(self):
        super().setUp()
        self._create_requirement_related_rows()

    def _create_requirement_related_rows(self):
        admin = get_user_model().objects.get(username="admin")
        audit = {"creation_user": admin, "change_user": admin}

        folders = {
            REQUIREMENT_1_FOLDER: {"requirement_id": 1},
            REQUIREMENT_2_FOLDER: {"requirement_id": 2},
            ITEM_1_FOLDER: {"requirement_item_id": 1},
            ITEM_2_FOLDER: {"requirement_item_id": 2},
        }
        for folder_id, owner in folders.items():
            Folder.objects.create(pk=folder_id, description="Root Level Folder", **owner, **audit)

        documents = [
            (REQUIREMENT_1_LINK, True, {"requirement_id": 1}),
            (REQUIREMENT_1_FILE, False, {"requirement_id": 1}),
            (REQUIREMENT_2_FILE, False, {"requirement_id": 2}),
            (REQUIREMENT_2_LINK, True, {"requirement_id": 2}),
            (ITEM_1_LINK, True, {"requirement_item_id": 1}),
            (ITEM_1_FILE, False, {"requirement_item_id": 1}),
            (ITEM_2_FILE, False, {"requirement_item_id": 2}),
            (ITEM_2_LINK, True, {"requirement_item_id": 2}),
        ]
        for key, is_link, owner in documents:
            if is_link:
                document = Document.objects.create(
                    key=key, description="NearBeach Homepage", url_location="https://nearbeach.org",
                    upload_successfully=True, **audit,
                )
            else:
                document = Document.objects.create(
                    key=key, description="nearbeach_logo.jpg", document=f"private/{key}/nearbeach_logo.jpg",
                    upload_successfully=True, **audit,
                )
            DocumentPermission.objects.create(document=document, **owner, **audit)

        item_links = {
            ITEM_1_LINK_ROW: {"requirement_item_id": 1, "task_id": 1},
            ITEM_2_LINK_ROW: {"requirement_item_id": 2, "task_id": 1},
            ITEM_2_OTHER_LINK_ROW: {"requirement_item_id": 2, "task_id": 2},
        }
        for row_id, owner in item_links.items():
            ObjectAssignment.objects.create(
                pk=row_id, link_relationship="Relate", parent_link="requirement_item", **owner, **audit
            )
