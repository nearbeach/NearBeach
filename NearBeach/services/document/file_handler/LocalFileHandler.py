import shutil

from NearBeach.services.document.file_handler.FileHandler import FileHandler
from pathlib import Path
from django.http import FileResponse


class LocalFileHandler(FileHandler):
    def __init__(self, local_settings):
        self.root = Path(local_settings.PRIVATE_MEDIA_ROOT)

    def fetch(self, document_results):
        # Normal setup - find document on server and serve
        # Get the Document path information
        file = self.root / str(document_results.document)
        return FileResponse(open(file, 'rb'))

    def upload(self, upload_document, document_results, file):
        """
        This function will upload the file and store it in the private folder destination under a subfolder that
        contains the same document_key value.
        :param upload_document: The FILE itself - to be uploaded
        :param document_results: The document_results - with variables we require
        :return:
        """
        # Make the directory we want to save the file in. The directory will have the document_key
        file_permissions = 0o755  # Look at these permissions later
        storage_location = self.root / str(document_results.document)
        storage_location.parent.mkdir(mode=file_permissions, exist_ok=True)

        # Save the upload document in the location
        with open(storage_location, "wb+") as destination:
            for chunk in upload_document.chunks():
                destination.write(chunk)

    def delete(self, document_key_id):
        storage_location = self.root / "private" / str(document_key_id)
        shutil.rmtree(storage_location, ignore_errors=True)