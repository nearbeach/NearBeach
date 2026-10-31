"""The classes that store, serve and delete uploaded files: local disk, S3 / MinIO / R2 and Azure.

The S3 and Azure clients are always mocked - these tests never touch a network or a bucket.
"""
import io
import shutil
import tempfile
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import Http404
from django.test import SimpleTestCase

from NearBeach.models.document.document import Document
from NearBeach.services.document.file_handler.AzureFileHandler import AzureFileHandler
from NearBeach.services.document.file_handler.GetFileHandler import get_file_handler
from NearBeach.services.document.file_handler.LocalFileHandler import LocalFileHandler
from NearBeach.services.document.file_handler.S3FileHandler import S3FileHandler

S3_MODULE = "NearBeach.services.document.file_handler.S3FileHandler"
AZURE_MODULE = "NearBeach.services.document.file_handler.AzureFileHandler"


def make_document(description="report.pdf"):
    key = uuid.uuid4()
    return Document(key=key, description=description, document=f"private/{key}/{description}")


def stream(response):
    return b"".join(response.streaming_content)


class LocalFileHandlerTests(SimpleTestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.handler = LocalFileHandler(SimpleNamespace(PRIVATE_MEDIA_ROOT=str(self.root)))

    def test_the_root_is_a_path(self):
        self.assertEqual(self.handler.root, self.root)

    def test_upload_then_fetch_gives_the_same_bytes(self):
        (self.root / "private").mkdir()
        document = make_document()
        upload = SimpleUploadedFile("report.pdf", b"%PDF contents")

        self.handler.upload(upload, document, upload)
        response = self.handler.fetch(document)

        self.assertEqual(stream(response), b"%PDF contents")

    def test_upload_stores_the_file_under_its_document_key(self):
        (self.root / "private").mkdir()
        document = make_document()

        self.handler.upload(SimpleUploadedFile("report.pdf", b"x"), document, None)

        self.assertTrue((self.root / "private" / str(document.key) / "report.pdf").is_file())

    def test_a_large_upload_is_written_in_full(self):
        (self.root / "private").mkdir()
        document = make_document()
        content = b"0123456789" * 100_000  # several chunks

        self.handler.upload(SimpleUploadedFile("big.bin", content), document, None)

        self.assertEqual((self.root / str(document.document)).read_bytes(), content)

    def test_upload_creates_the_private_folder_on_a_fresh_install(self):
        """The first ever upload used to fail with FileNotFoundError when root/private did not exist yet"""
        document = make_document()

        self.handler.upload(SimpleUploadedFile("report.pdf", b"first"), document, None)

        self.assertEqual((self.root / str(document.document)).read_bytes(), b"first")

    def test_uploading_twice_replaces_the_file(self):
        (self.root / "private").mkdir()
        document = make_document()

        self.handler.upload(SimpleUploadedFile("report.pdf", b"one"), document, None)
        self.handler.upload(SimpleUploadedFile("report.pdf", b"two"), document, None)

        self.assertEqual((self.root / str(document.document)).read_bytes(), b"two")

    def test_fetching_a_missing_file_is_a_404_not_a_crash(self):
        with self.assertRaises(Http404):
            self.handler.fetch(make_document())

    def test_delete_removes_the_documents_folder_only(self):
        (self.root / "private").mkdir()
        keep, remove = make_document("keep.txt"), make_document("remove.txt")
        for document in (keep, remove):
            self.handler.upload(SimpleUploadedFile("f.txt", b"x"), document, None)

        self.handler.delete(remove.key)

        self.assertFalse((self.root / "private" / str(remove.key)).exists())
        self.assertTrue((self.root / "private" / str(keep.key)).exists())

    def test_deleting_something_that_is_not_there_is_fine(self):
        self.handler.delete(uuid.uuid4())

    def test_delete_accepts_a_uuid_or_a_string(self):
        (self.root / "private").mkdir()
        for as_text in (False, True):
            document = make_document()
            self.handler.upload(SimpleUploadedFile("f.txt", b"x"), document, None)

            self.handler.delete(str(document.key) if as_text else document.key)

            self.assertFalse((self.root / "private" / str(document.key)).exists())


class S3FileHandlerTests(SimpleTestCase):
    settings = SimpleNamespace(
        AWS_ACCESS_KEY_ID="key-id",
        AWS_SECRET_ACCESS_KEY="secret",
        AWS_STORAGE_BUCKET_NAME="my-bucket",
    )

    def _handler(self, **extra):
        with mock.patch(f"{S3_MODULE}.boto3.client") as client:
            handler = S3FileHandler(SimpleNamespace(**{**vars(self.settings), **extra}))

        return handler, client

    def test_it_connects_with_the_keys_and_remembers_the_bucket(self):
        handler, client = self._handler()

        client.assert_called_once_with("s3", aws_access_key_id="key-id", aws_secret_access_key="secret")
        self.assertEqual(handler._bucket, "my-bucket")

    def test_an_endpoint_url_means_minio_so_the_connection_is_checked(self):
        with mock.patch(f"{S3_MODULE}.boto3.client") as client:
            S3FileHandler(SimpleNamespace(**vars(self.settings), AWS_S3_ENDPOINT_URL="http://minio:9000"))

        self.assertEqual(client.call_count, 2)  # one to check the connection, one to use
        for call in client.call_args_list:
            self.assertEqual(call.kwargs["endpoint_url"], "http://minio:9000")
        client.return_value.list_buckets.assert_called_once()

    def test_an_unreachable_endpoint_is_reported_but_does_not_stop_start_up(self):
        with mock.patch(f"{S3_MODULE}.boto3.client") as client, mock.patch("builtins.print") as printed:
            client.return_value.list_buckets.side_effect = ConnectionError("no route to host")

            S3FileHandler(SimpleNamespace(**vars(self.settings), AWS_S3_ENDPOINT_URL="http://minio:9000"))

        self.assertIn("no route to host", printed.call_args.args[0])

    def test_upload_sends_the_file_to_the_bucket_under_its_path(self):
        handler, _ = self._handler()
        document, upload = make_document(), SimpleUploadedFile("report.pdf", b"x")

        handler.upload(upload, document, upload)

        handler._s3.upload_fileobj.assert_called_once_with(upload, "my-bucket", str(document.document))

    def test_fetch_streams_the_object_as_an_attachment_named_after_the_document(self):
        handler, _ = self._handler()
        handler._s3.get_object.return_value = {"Body": io.BytesIO(b"bucket bytes")}
        document = make_document("quarterly report.pdf")

        response = handler.fetch(document)

        handler._s3.get_object.assert_called_once_with(Bucket="my-bucket", Key=str(document.document))
        self.assertEqual(stream(response), b"bucket bytes")
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertIn("quarterly report.pdf", response["Content-Disposition"])

    def test_delete_removes_every_object_under_the_documents_prefix(self):
        handler, _ = self._handler()
        key = uuid.uuid4()
        handler._s3.list_objects.return_value = {
            "Contents": [{"Key": f"private/{key}/a.pdf"}, {"Key": f"private/{key}/b.pdf"}]
        }

        handler.delete(key)

        handler._s3.list_objects.assert_called_once_with(Bucket="my-bucket", Prefix=f"private/{key}")
        handler._s3.delete_objects.assert_called_once_with(
            Bucket="my-bucket",
            Delete={"Objects": [{"Key": f"private/{key}/a.pdf"}, {"Key": f"private/{key}/b.pdf"}]},
        )

    def test_delete_with_nothing_to_delete_does_not_call_s3_with_an_empty_list(self):
        """S3 rejects delete_objects with no objects (MalformedXML)"""
        handler, _ = self._handler()
        handler._s3.list_objects.return_value = {}

        handler.delete(uuid.uuid4())

        handler._s3.delete_objects.assert_not_called()


class AzureFileHandlerTests(SimpleTestCase):
    settings = SimpleNamespace(
        AZURE_STORAGE_CONNECTION_STRING="UseDevelopmentStorage=true",
        AZURE_STORAGE_CONTAINER_NAME="documents",
    )

    def _handler(self):
        with mock.patch(f"{AZURE_MODULE}.BlobServiceClient") as service:
            handler = AzureFileHandler(self.settings)

        return handler, service

    def test_it_connects_with_the_connection_string(self):
        _, service = self._handler()

        service.from_connection_string.assert_called_once_with("UseDevelopmentStorage=true")

    def test_upload_puts_the_file_in_the_container_under_its_path(self):
        handler, _ = self._handler()
        document, upload = make_document(), SimpleUploadedFile("report.pdf", b"x")

        handler.upload(upload, document, upload)

        handler._service_client.get_blob_client.assert_called_once_with(
            container="documents", blob=str(document.document)
        )
        handler._service_client.get_blob_client.return_value.upload_blob.assert_called_once_with(upload)

    def test_fetch_returns_the_blob_as_an_attachment_named_after_the_document(self):
        handler, _ = self._handler()
        container = handler._service_client.get_container_client.return_value
        container.download_blob.return_value.readall.return_value = b"azure bytes"
        document = make_document("minutes.docx")

        response = handler.fetch(document)

        handler._service_client.get_container_client.assert_called_once_with(container="documents")
        container.download_blob.assert_called_once_with(str(document.document))
        self.assertEqual(stream(response), b"azure bytes")
        self.assertIn("minutes.docx", response["Content-Disposition"])

    def test_delete_removes_every_blob_under_the_documents_prefix(self):
        handler, _ = self._handler()
        key = uuid.uuid4()
        container = handler._service_client.get_container_client.return_value
        container.list_blobs.return_value = [SimpleNamespace(name=f"private/{key}/a"), SimpleNamespace(name=f"private/{key}/b")]

        handler.delete(key)

        container.list_blobs.assert_called_once_with(name_starts_with=f"private/{key}")
        deleted = [call.kwargs["blob"] for call in handler._service_client.get_blob_client.call_args_list]
        self.assertEqual(deleted, [f"private/{key}/a", f"private/{key}/b"])
        self.assertEqual(handler._service_client.get_blob_client.return_value.delete_blob.call_count, 2)

    def test_delete_with_no_blobs_does_nothing(self):
        handler, _ = self._handler()
        handler._service_client.get_container_client.return_value.list_blobs.return_value = []

        handler.delete(uuid.uuid4())

        handler._service_client.get_blob_client.assert_not_called()


class GetFileHandlerTests(SimpleTestCase):
    """Which handler a deployment gets, decided by the settings it provides"""

    @staticmethod
    def _pick(**local_settings):
        with mock.patch(f"{S3_MODULE}.boto3.client"), mock.patch(f"{AZURE_MODULE}.BlobServiceClient"):
            return get_file_handler(SimpleNamespace(PRIVATE_MEDIA_ROOT="/tmp/nearbeach", **local_settings))

    S3 = dict(AWS_ACCESS_KEY_ID="k", AWS_SECRET_ACCESS_KEY="s", AWS_STORAGE_BUCKET_NAME="b")
    AZURE = dict(AZURE_STORAGE_CONNECTION_STRING="c", AZURE_STORAGE_CONTAINER_NAME="n")

    def test_no_cloud_settings_means_local_disk(self):
        self.assertIsInstance(self._pick(), LocalFileHandler)

    def test_aws_settings_mean_s3(self):
        self.assertIsInstance(self._pick(**self.S3), S3FileHandler)

    def test_azure_settings_mean_azure(self):
        self.assertIsInstance(self._pick(**self.AZURE), AzureFileHandler)

    def test_s3_wins_when_both_are_set(self):
        self.assertIsInstance(self._pick(**self.S3, **self.AZURE), S3FileHandler)

    def test_empty_values_do_not_count_as_configured(self):
        self.assertIsInstance(self._pick(AWS_ACCESS_KEY_ID="", AZURE_STORAGE_CONNECTION_STRING=None), LocalFileHandler)
