"""Who can fetch /private/<document key>/ - the route every uploaded file and document link is served from.

Fixture data (see NearBeach_basic_setup.json):
 - project 2 ("Project - QA Team", group 2): uploaded file 17f494c7... and link 93ac2002...
 - project 1 (group 1 only):                 uploaded file 5390175c... and link 277b25be...
 - users: admin and dark_admin are superusers (dark_admin is only in group 1); team_leader, team_member,
   team_intern, read_only and read_only_extra are in group 2; no_group is in no group
A user who may not see a document is told it does not exist (404, never 403) so keys can not be probed.
"""
import shutil
import tempfile
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from django.contrib.auth.models import User
from django.test import Client, TestCase

from NearBeach.models.document.document import Document
from NearBeach.models.document.document_permission import DocumentPermission
from NearBeach.models.user import UserProfilePicture
from NearBeach.services.document.file_handler.LocalFileHandler import LocalFileHandler

PASSWORD = "Test1234$"

QA_FILE = "17f494c7-067e-4f70-b944-64439d9101a7"
QA_LINK = "93ac2002-ff86-4835-9607-65037279c8b9"
ADMIN_FILE = "5390175c-82e6-47cb-b9ae-91d88a323868"
ADMIN_LINK = "277b25be-7913-4432-968f-fa3c699956f3"
UNKNOWN_KEY = "00000000-0000-4000-8000-000000000000"

QA_USERS = ["team_leader", "team_member", "team_intern", "read_only", "read_only_extra"]


class PrivateDocumentViewTests(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        # Serve files from a temp folder with the local handler - never from a bucket
        self.storage = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.storage, ignore_errors=True)
        for key, content in {QA_FILE: b"qa file", ADMIN_FILE: b"admin file"}.items():
            document = Document.objects.get(pk=key)
            path = self.storage / str(document.document)
            path.parent.mkdir(parents=True)
            path.write_bytes(content)

        handler = LocalFileHandler(SimpleNamespace(PRIVATE_MEDIA_ROOT=self.storage))
        patcher = mock.patch("NearBeach.views.private_document.private_document_views.FILE_HANDLER", handler)
        patcher.start()
        self.addCleanup(patcher.stop)

    def _client(self, username=None):
        client = Client()
        if username is not None:
            self.assertTrue(client.login(username=username, password=PASSWORD), username)
        return client

    def _get(self, key, username=None):
        return self._client(username).get(f"/private/{key}/")

    @staticmethod
    def _content(response):
        return b"".join(response.streaming_content)

    # ---------- not logged in ----------
    def test_anonymous_users_are_sent_to_log_in(self):
        for key in (QA_FILE, QA_LINK, UNKNOWN_KEY):
            with self.subTest(key=key):
                response = self._get(key)

                self.assertEqual(response.status_code, 302)
                self.assertTrue(response["Location"].startswith("/private/?next="))

    # ---------- users in the project's group ----------
    def test_group_members_get_the_uploaded_file(self):
        for username in QA_USERS:
            with self.subTest(username=username):
                response = self._get(QA_FILE, username)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(self._content(response), b"qa file")

    def test_group_members_are_redirected_to_a_link(self):
        for username in QA_USERS:
            with self.subTest(username=username):
                response = self._get(QA_LINK, username)

                self.assertEqual(response.status_code, 302)
                self.assertEqual(response["Location"], Document.objects.get(pk=QA_LINK).url_location)

    # ---------- users outside the project's group ----------
    def test_users_in_another_group_get_a_404(self):
        for username in QA_USERS:
            for key in (ADMIN_FILE, ADMIN_LINK):
                with self.subTest(username=username, key=key):
                    self.assertEqual(self._get(key, username).status_code, 404)

    def test_a_user_with_no_group_gets_a_404(self):
        for key in (QA_FILE, QA_LINK, ADMIN_FILE, ADMIN_LINK):
            with self.subTest(key=key):
                self.assertEqual(self._get(key, "no_group").status_code, 404)

    def test_removing_the_document_permission_removes_access(self):
        DocumentPermission.objects.filter(document_id=QA_FILE).update(is_deleted=True)

        self.assertEqual(self._get(QA_FILE, "team_leader").status_code, 404)

    # ---------- superusers ----------
    def test_superusers_can_get_every_document(self):
        """dark_admin is only in the Administration group - being a superuser is what lets them in"""
        for username in ("admin", "dark_admin"):
            for key, content in {QA_FILE: b"qa file", ADMIN_FILE: b"admin file"}.items():
                with self.subTest(username=username, key=key):
                    response = self._get(key, username)

                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(self._content(response), content)

    def test_unknown_keys_are_a_404_for_everyone(self):
        for username in ("team_leader", "no_group", "admin"):
            with self.subTest(username=username):
                self.assertEqual(self._get(UNKNOWN_KEY, username).status_code, 404)

    # ---------- documents that are not attached to an object ----------
    @staticmethod
    def _link_document(**permission):
        user = User.objects.get(username="admin")
        document = Document.objects.create(
            change_user=user,
            creation_user=user,
            description="Detached link",
            url_location="https://example.org/detached",
            upload_successfully=True,
        )
        if permission:
            DocumentPermission.objects.create(
                change_user=user, creation_user=user, document=document, **permission
            )

        return document

    def test_profile_pictures_can_be_seen_by_any_logged_in_user(self):
        document = self._link_document()
        admin = User.objects.get(username="admin")
        UserProfilePicture.objects.create(
            username=admin, document=document, change_user=admin, creation_user=admin
        )

        for username in ("no_group", "team_leader"):
            with self.subTest(username=username):
                self.assertEqual(self._get(document.key, username).status_code, 302)

        self.assertEqual(self._get(document.key).status_code, 302)  # anonymous: sent to log in, not served
        self.assertTrue(self._get(document.key)["Location"].startswith("/private/?next="))

    def test_organisation_and_customer_pictures_can_be_seen_by_any_logged_in_user(self):
        for field, pk in (("organisation_id", 1), ("customer_id", 1)):
            document = self._link_document(**{field: pk})
            with self.subTest(field=field):
                self.assertEqual(self._get(document.key, "no_group").status_code, 302)
                self.assertEqual(
                    self._get(document.key, "no_group")["Location"], "https://example.org/detached"
                )

    def test_a_picture_for_a_new_object_can_be_seen_by_any_logged_in_user(self):
        """Uploaded while the object is still being created - the only thing set is the new_object uuid"""
        document = self._link_document(new_object=uuid.uuid4())

        self.assertEqual(self._get(document.key, "no_group").status_code, 302)

    def test_a_document_with_no_permission_at_all_is_only_for_superusers(self):
        document = self._link_document()

        self.assertEqual(self._get(document.key, "team_leader").status_code, 404)
        self.assertEqual(self._get(document.key, "admin").status_code, 302)
