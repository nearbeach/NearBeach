"""CRUD tests for the documents, links and folders of a project, run as the team leader.

Fixture data for project 2 ("Project - QA Team"):
 - folders 3 ("Root Level Folder") and 4 ("Sub Folder", inside 3)
 - links 93ac2002... (root) and ea6fb519... (in folder 3)
 - uploaded files 17f494c7... (root) and a3cb3749... (in folder 3)
 - one more link, 80a7bd50..., whose upload never finished - it is never listed
Project 1 has its own documents and folders (1 and 2).
"""
import shutil
import tempfile
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from NearBeach.models.document.document import Document
from NearBeach.models.document.document_permission import DocumentPermission
from NearBeach.models.document.folder import Folder
from NearBeach.services.document.file_handler import HandleDocumentPermissions
from NearBeach.services.document.file_handler.LocalFileHandler import LocalFileHandler
from NearBeach.tests.tests_api.tests_crud.test_team_leader.test_crud_project import (
    QA_PROJECT_URL,
    TeamLeaderProjectBase,
)

DOCUMENTS_URL = f"{QA_PROJECT_URL}documents/"

ROOT_FOLDER, SUB_FOLDER, OTHER_PROJECT_FOLDER = 3, 4, 1

ROOT_LINK = "93ac2002-ff86-4835-9607-65037279c8b9"
FOLDER_LINK = "ea6fb519-bf03-4f1f-a8e3-b9c73979797b"
ROOT_FILE = "17f494c7-067e-4f70-b944-64439d9101a7"
FOLDER_FILE = "a3cb3749-91cf-4b07-9e21-35b4278d3ce4"
UNFINISHED_LINK = "80a7bd50-eba9-49f8-a55c-d1febd052ab9"
OTHER_PROJECT_LINK = "e6bfcfe9-a5c9-4dc2-a634-7067aa3dc666"  # project 1


class ProjectDocumentBase(TeamLeaderProjectBase):
    def setUp(self):
        super().setUp()
        # Uploaded files are written under the file handler's root - keep them out of the repository.
        # Always use the local handler: the real one depends on the machine's .env (S3 / Azure settings)
        # and these tests must never talk to a bucket.
        self.storage = Path(tempfile.mkdtemp())
        (self.storage / "private").mkdir()
        local_handler = LocalFileHandler(SimpleNamespace(PRIVATE_MEDIA_ROOT=self.storage))
        patcher = mock.patch.object(HandleDocumentPermissions, "FILE_HANDLER", local_handler)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(shutil.rmtree, self.storage, ignore_errors=True)

    def _list(self):
        return self.client.get(DOCUMENTS_URL).data

    def _document_keys(self):
        return sorted(str(document["key"]) for document in self._list()["documents"])

    def _folder_ids(self):
        return sorted(folder["id"] for folder in self._list()["folders"])

    def _create_folder(self, description="Leader folder", **extra):
        return self.client.post(
            DOCUMENTS_URL, {"type": "folder", "description": description, **extra}, format="json"
        )

    def _create_link(self, description="Leader link", url="https://example.org/leader", **extra):
        return self.client.post(
            DOCUMENTS_URL,
            {"type": "link", "description": description, "url_location": url, **extra},
            format="json",
        )

    def _upload(self, name="report.txt", content=b"hello", description="Leader upload", **extra):
        return self.client.post(
            DOCUMENTS_URL,
            {"type": "document", "description": description, "document": SimpleUploadedFile(name, content), **extra},
            format="multipart",
        )

    def _delete(self, key, doc_type):
        return self.client.delete(f"{DOCUMENTS_URL}{key}/", {"type": doc_type}, format="json")


class ProjectDocumentListTests(ProjectDocumentBase):
    def test_list_has_the_documents_folders_and_upload_limit(self):
        response = self.client.get(DOCUMENTS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.data), {"documents", "folders", "max_upload_size"})
        self.assertIsInstance(response.data["max_upload_size"], int)

    def test_list_has_the_links_and_files_of_the_project(self):
        self.assertEqual(
            self._document_keys(),
            sorted([ROOT_LINK, FOLDER_LINK, ROOT_FILE, FOLDER_FILE]),
        )

    def test_list_has_the_folders_of_the_project(self):
        self.assertEqual(self._folder_ids(), [ROOT_FOLDER, SUB_FOLDER])

    def test_document_rows_have_the_documented_fields(self):
        rows = {str(d["key"]): d for d in self._list()["documents"]}

        link = rows[FOLDER_LINK]
        self.assertEqual(link["description"], "NearBeach Blogs")
        self.assertEqual(link["url_location"], "https://nearbeach.org/blogs")
        self.assertEqual(link["parent_folder_id"], ROOT_FOLDER)
        self.assertIsNone(rows[ROOT_LINK]["parent_folder_id"])
        self.assertEqual(rows[ROOT_FILE]["description"], "nearbeach_logo.jpg")

    def test_folder_rows_have_the_documented_fields(self):
        folders = {f["id"]: f for f in self._list()["folders"]}

        self.assertEqual(folders[ROOT_FOLDER]["description"], "Root Level Folder")
        self.assertIsNone(folders[ROOT_FOLDER]["parent_folder_id"])
        self.assertEqual(folders[SUB_FOLDER]["parent_folder_id"], ROOT_FOLDER)

    def test_unfinished_uploads_and_other_projects_are_not_listed(self):
        keys = self._document_keys()

        self.assertNotIn(UNFINISHED_LINK, keys)
        self.assertNotIn(OTHER_PROJECT_LINK, keys)
        self.assertNotIn(OTHER_PROJECT_FOLDER, self._folder_ids())

    def test_deleted_documents_and_folders_are_not_listed(self):
        Document.objects.filter(pk=ROOT_LINK).update(is_deleted=True)
        Folder.objects.filter(pk=SUB_FOLDER).update(is_deleted=True)

        self.assertNotIn(ROOT_LINK, self._document_keys())
        self.assertEqual(self._folder_ids(), [ROOT_FOLDER])

    def test_missing_project_is_not_found(self):
        self.assertEqual(self.client.get("/api/v1/project/9999/documents/").status_code, 404)


class ProjectFolderTests(ProjectDocumentBase):
    # ---------- create ----------
    def test_create_returns_the_folder(self):
        response = self._create_folder("New folder")

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["description"], "New folder")
        self.assertIsNone(response.data["parent_folder_id"])

    def test_create_saves_the_folder_against_the_project(self):
        folder = Folder.objects.get(pk=self._create_folder("New folder").data["id"])

        self.assertEqual(folder.project_id, 2)
        self.assertEqual(folder.description, "New folder")
        self.assertIsNone(folder.parent_folder_id)
        self.assertEqual(folder.creation_user, self.leader)
        self.assertEqual(folder.change_user, self.leader)
        self.assertFalse(folder.is_deleted)

    def test_create_inside_another_folder(self):
        response = self._create_folder("Inside", parent_folder_id=ROOT_FOLDER)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["parent_folder_id"], ROOT_FOLDER)
        self.assertEqual(Folder.objects.get(pk=response.data["id"]).parent_folder_id, ROOT_FOLDER)

    def test_a_new_folder_appears_in_the_list(self):
        created = self._create_folder().data["id"]

        self.assertEqual(self._folder_ids(), [ROOT_FOLDER, SUB_FOLDER, created])

    def test_create_does_not_touch_other_projects(self):
        before = Folder.objects.filter(project_id=1).count()

        self._create_folder()

        self.assertEqual(Folder.objects.filter(project_id=1).count(), before)

    def test_bad_folders_are_rejected_and_nothing_is_saved(self):
        bodies = {
            "no description": {"type": "folder"},
            "blank description": {"type": "folder", "description": ""},
            "no type": {"description": "x"},
            "unknown type": {"type": "banana", "description": "x"},
            "bad parent": {"type": "folder", "description": "x", "parent_folder_id": "abc"},
        }
        before = Folder.objects.count()

        for name, body in bodies.items():
            with self.subTest(name):
                self.assertEqual(self.client.post(DOCUMENTS_URL, body, format="json").status_code, 400)

        self.assertEqual(Folder.objects.count(), before)

    # ---------- update ----------
    def _patch(self, folder_id, **body):
        return self.client.patch(
            f"{DOCUMENTS_URL}{folder_id}/", {"type": "folder", "description": "Renamed", **body}, format="json"
        )

    def test_renaming_a_folder(self):
        response = self._patch(ROOT_FOLDER)

        self.assertEqual(response.status_code, 200, response.data)
        folder = Folder.objects.get(pk=ROOT_FOLDER)
        self.assertEqual(folder.description, "Renamed")
        self.assertEqual(folder.change_user, self.leader)

    def test_renaming_moves_date_modified_forward(self):
        before = Folder.objects.get(pk=ROOT_FOLDER).date_modified

        self._patch(ROOT_FOLDER)

        self.assertGreater(Folder.objects.get(pk=ROOT_FOLDER).date_modified, before)

    def test_renaming_leaves_the_other_folders_alone(self):
        self._patch(ROOT_FOLDER)

        self.assertEqual(Folder.objects.get(pk=SUB_FOLDER).description, "Sub Folder")
        self.assertEqual(Folder.objects.get(pk=OTHER_PROJECT_FOLDER).description, "Folder at root")

    def test_moving_a_folder_into_another_folder(self):
        """Regression - FolderService.update looked for "parent_folder" but the serializer sends "parent_folder_id",
        so a folder could be renamed but never moved"""
        self._patch(ROOT_FOLDER, parent_folder_id=SUB_FOLDER)

        self.assertEqual(Folder.objects.get(pk=ROOT_FOLDER).parent_folder_id, SUB_FOLDER)

    def test_folders_that_are_not_on_this_project_cannot_be_updated(self):
        for folder_id in (9999, OTHER_PROJECT_FOLDER):
            with self.subTest(folder_id=folder_id):
                self.assertEqual(self._patch(folder_id).status_code, 400)

        self.assertEqual(Folder.objects.get(pk=OTHER_PROJECT_FOLDER).description, "Folder at root")

    # ---------- delete ----------
    def test_deleting_a_folder(self):
        response = self._delete(SUB_FOLDER, "folder")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(self._folder_ids(), [ROOT_FOLDER])

    def test_delete_is_a_soft_delete(self):
        self._delete(SUB_FOLDER, "folder")

        folder = Folder.objects.get(pk=SUB_FOLDER)
        self.assertTrue(folder.is_deleted)
        self.assertEqual(folder.change_user, self.leader)

    def test_deleting_a_folder_needs_the_type(self):
        response = self.client.delete(f"{DOCUMENTS_URL}{SUB_FOLDER}/", {}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Folder.objects.get(pk=SUB_FOLDER).is_deleted)

    def test_deleting_twice_is_rejected(self):
        self._delete(SUB_FOLDER, "folder")

        self.assertEqual(self._delete(SUB_FOLDER, "folder").status_code, 400)

    def test_folders_that_are_not_on_this_project_cannot_be_deleted(self):
        for folder_id in (9999, OTHER_PROJECT_FOLDER):
            with self.subTest(folder_id=folder_id):
                self.assertEqual(self._delete(folder_id, "folder").status_code, 400)

        self.assertFalse(Folder.objects.get(pk=OTHER_PROJECT_FOLDER).is_deleted)

    def test_deleting_a_folder_leaves_its_contents_in_place(self):
        """Nothing cascades - the documents stay, but now point at a folder that is gone"""
        self._delete(ROOT_FOLDER, "folder")

        self.assertIn(FOLDER_LINK, self._document_keys())
        self.assertFalse(Folder.objects.get(pk=SUB_FOLDER).is_deleted)

    def test_delete_missing_project_is_not_found(self):
        response = self.client.delete("/api/v1/project/9999/documents/3/", {"type": "folder"}, format="json")

        self.assertEqual(response.status_code, 404)


class ProjectDocumentLinkTests(ProjectDocumentBase):
    # ---------- create ----------
    def test_create_returns_the_link(self):
        response = self._create_link("My link", "https://example.org/mine")

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["description"], "My link")
        self.assertEqual(response.data["url_location"], "https://example.org/mine")
        self.assertIsNone(response.data["parent_folder_id"])
        uuid.UUID(str(response.data["key"]))

    def test_create_saves_the_link_against_the_project(self):
        key = self._create_link("My link", "https://example.org/mine").data["key"]

        document = Document.objects.get(pk=key)
        self.assertEqual(document.description, "My link")
        self.assertEqual(document.url_location, "https://example.org/mine")
        self.assertTrue(document.upload_successfully)
        self.assertEqual(document.creation_user, self.leader)
        self.assertEqual(document.change_user, self.leader)

        permission = DocumentPermission.objects.get(document=document)
        self.assertEqual(permission.project_id, 2)
        self.assertIsNone(permission.folder_id)
        self.assertFalse(permission.is_profile_picture)

    def test_create_inside_a_folder(self):
        response = self._create_link(parent_folder_id=ROOT_FOLDER)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["parent_folder_id"], ROOT_FOLDER)
        self.assertEqual(DocumentPermission.objects.get(document_id=response.data["key"]).folder_id, ROOT_FOLDER)

    def test_a_new_link_appears_in_the_list(self):
        key = str(self._create_link().data["key"])

        self.assertIn(key, self._document_keys())

    def test_create_does_not_touch_other_projects(self):
        before = DocumentPermission.objects.filter(project_id=1).count()

        self._create_link()

        self.assertEqual(DocumentPermission.objects.filter(project_id=1).count(), before)

    def test_bad_links_are_rejected_and_nothing_is_saved(self):
        bodies = {
            "no url": {"type": "link", "description": "x"},
            "no description": {"type": "link", "url_location": "https://example.org"},
            "blank description": {"type": "link", "description": "", "url_location": "https://example.org"},
        }
        before = Document.objects.count()

        for name, body in bodies.items():
            with self.subTest(name):
                self.assertEqual(self.client.post(DOCUMENTS_URL, body, format="json").status_code, 400)

        self.assertEqual(Document.objects.count(), before)

    # ---------- update ----------
    def test_updating_a_link(self):
        """Regression - DocumentLinkService.update filtered Document by project_id/folder, which live on
        DocumentPermission, so it raised a FieldError"""
        response = self.client.patch(
            f"{DOCUMENTS_URL}{ROOT_LINK}/",
            {"type": "link", "description": "Renamed link", "url_location": "https://example.org/new"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Document.objects.get(pk=ROOT_LINK).description, "Renamed link")

    # ---------- delete ----------
    def test_deleting_a_link(self):
        response = self._delete(ROOT_LINK, "link")

        self.assertEqual(response.status_code, 204)
        self.assertNotIn(ROOT_LINK, self._document_keys())

    def test_delete_is_a_soft_delete_of_the_link_and_its_permission(self):
        self._delete(ROOT_LINK, "link")

        document = Document.objects.get(pk=ROOT_LINK)
        self.assertTrue(document.is_deleted)
        self.assertEqual(document.change_user, self.leader)
        permission = DocumentPermission.objects.get(document_id=ROOT_LINK)
        self.assertTrue(permission.is_deleted)
        self.assertEqual(permission.change_user, self.leader)

    def test_deleting_a_link_leaves_the_others_alone(self):
        self._delete(ROOT_LINK, "link")

        self.assertEqual(self._document_keys(), sorted([FOLDER_LINK, ROOT_FILE, FOLDER_FILE]))

    def test_deleting_twice_is_rejected(self):
        self._delete(ROOT_LINK, "link")

        self.assertEqual(self._delete(ROOT_LINK, "link").status_code, 400)

    def test_links_that_are_not_on_this_project_cannot_be_deleted(self):
        for key in (str(uuid.uuid4()), OTHER_PROJECT_LINK):
            with self.subTest(key=key):
                self.assertEqual(self._delete(key, "link").status_code, 400)

        self.assertFalse(Document.objects.get(pk=OTHER_PROJECT_LINK).is_deleted)

    def test_delete_missing_project_is_not_found(self):
        response = self.client.delete(f"/api/v1/project/9999/documents/{ROOT_LINK}/", {"type": "link"}, format="json")

        self.assertEqual(response.status_code, 404)


class ProjectDocumentUploadTests(ProjectDocumentBase):
    # ---------- create ----------
    def test_upload_returns_the_document(self):
        response = self._upload("report.txt", b"hello", "Quarterly report")

        self.assertEqual(response.status_code, 201, response.data)
        document = response.data[0]
        self.assertEqual(document["description"], "Quarterly report")
        uuid.UUID(str(document["key"]))
        self.assertIsNone(document["parent_folder_id"])

    def test_upload_saves_the_file_and_the_rows(self):
        key = self._upload("report.txt", b"hello").data[0]["key"]

        document = Document.objects.get(pk=key)
        self.assertTrue(document.upload_successfully)
        self.assertEqual(document.change_user, self.leader)
        self.assertEqual(str(document.document), f"private/{key}/report.txt")
        self.assertEqual((self.storage / str(document.document)).read_bytes(), b"hello")

        permission = DocumentPermission.objects.get(document=document)
        self.assertEqual(permission.project_id, 2)
        self.assertFalse(permission.is_profile_picture)

    def test_upload_inside_a_folder(self):
        response = self._upload(parent_folder_id=ROOT_FOLDER)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data[0]["parent_folder_id"], ROOT_FOLDER)

    def test_a_parent_folder_of_zero_means_the_root(self):
        response = self._upload(parent_folder_id=0)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertIsNone(response.data[0]["parent_folder_id"])

    def test_an_uploaded_file_appears_in_the_list(self):
        key = str(self._upload().data[0]["key"])

        self.assertIn(key, self._document_keys())

    def test_upload_does_not_touch_other_projects(self):
        before = DocumentPermission.objects.filter(project_id=1).count()

        self._upload()

        self.assertEqual(DocumentPermission.objects.filter(project_id=1).count(), before)

    def test_upload_needs_a_file_and_a_description(self):
        bodies = {
            "no file": {"type": "document", "description": "x"},
            "no description": {"type": "document", "document": SimpleUploadedFile("a.txt", b"a")},
        }
        before = Document.objects.count()

        for name, body in bodies.items():
            with self.subTest(name):
                self.assertEqual(self.client.post(DOCUMENTS_URL, body, format="multipart").status_code, 400)

        self.assertEqual(Document.objects.count(), before)
        self.assertEqual(list((self.storage / "private").iterdir()), [])

    @override_settings(MAX_FILE_SIZE_UPLOAD=4)
    def test_a_file_that_is_too_large_is_rejected(self):
        before = Document.objects.count()

        response = self._upload("big.txt", b"more than four bytes")

        self.assertEqual(response.status_code, 413)
        self.assertEqual(Document.objects.count(), before)
        self.assertEqual(list((self.storage / "private").iterdir()), [])

    @override_settings(MAX_FILE_SIZE_UPLOAD=5)
    def test_a_file_at_the_limit_is_accepted(self):
        self.assertEqual(self._upload("ok.txt", b"12345").status_code, 201)

    # ---------- update ----------
    def test_updating_an_uploaded_document(self):
        """Regression - DocumentService.update filtered DocumentPermission on document_key, which does not exist,
        so it raised a FieldError"""
        response = self.client.patch(
            f"{DOCUMENTS_URL}{ROOT_FILE}/",
            {"type": "document", "description": "Renamed file"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Document.objects.get(pk=ROOT_FILE).description, "Renamed file")

    # ---------- delete ----------
    def test_deleting_an_uploaded_document(self):
        """Regression - DocumentService.delete filtered Document on project_id, which lives on DocumentPermission, so
        it raised a FieldError. (A description is still accepted, but no longer demanded, on a delete.)"""
        response = self.client.delete(
            f"{DOCUMENTS_URL}{ROOT_FILE}/", {"type": "document", "description": "x"}, format="json"
        )

        self.assertEqual(response.status_code, 204)
        self.assertTrue(Document.objects.get(pk=ROOT_FILE).is_deleted)
        self.assertNotIn(ROOT_FILE, self._document_keys())

