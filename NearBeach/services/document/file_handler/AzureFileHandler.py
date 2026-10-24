from typing import Union, cast
from uuid import UUID

from azure.storage.blob import BlobServiceClient
from django.conf import LazySettings
from django.core.files.uploadedfile import UploadedFile
from django.core.files.base import ContentFile

from NearBeach.models.document.document import Document
from NearBeach.services.document.file_handler.FileHandler import FileHandler
from django.http import FileResponse


class AzureFileHandler(FileHandler):
    def __init__(self, local_settings: LazySettings) -> None:
        # get_file_handler only picks this handler when Azure is configured, so these are set
        # (mypy reads their types from local/settings.py, where they are optional)
        # Create the BlobServiceClient object
        self._service_client = BlobServiceClient.from_connection_string(
            cast(str, local_settings.AZURE_STORAGE_CONNECTION_STRING)
        )
        self._client_name = cast(str, local_settings.AZURE_STORAGE_CONTAINER_NAME)

    def fetch(self, document_results: Document) -> FileResponse:
        # Get container
        container_client = self._service_client.get_container_client(
            container=self._client_name
        )
        # Set up the file to send
        file_to_send = ContentFile(
            container_client.download_blob(
                str(document_results.document)
            ).readall()
        )
        # Return file
        return FileResponse(
            file_to_send,
            as_attachment=True,
            filename=document_results.description,
        )

    def upload(self, upload_document: UploadedFile, document_results: Document, file: UploadedFile) -> None:
        # Create the blob client using the private file path name as the name for the blob
        blob_client = self._service_client.get_blob_client(
            container=self._client_name,
            blob=str(document_results.document),
        )
        # Upload the created file
        blob_client.upload_blob(file)

    def delete(self, document_key_id: Union[UUID, str]) -> None:
        container_client = self._service_client.get_container_client(
            container=self._client_name
        )

        blob_list = container_client.list_blobs(
            name_starts_with=F"private/{document_key_id}"
        )

        for blob in blob_list:
            blob_client = self._service_client.get_blob_client(
                container=self._client_name,
                blob=blob.name
            )
            blob_client.delete_blob()