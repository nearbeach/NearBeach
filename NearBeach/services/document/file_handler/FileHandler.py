from abc import ABC, abstractmethod
from typing import Union
from uuid import UUID

from django.core.files.uploadedfile import UploadedFile
from django.http import FileResponse

from NearBeach.models.document.document import Document


class FileHandler(ABC):
    """Abstraction for file handler classes"""

    @abstractmethod
    def upload(self, upload_document: UploadedFile, document_results: Document, file: UploadedFile) -> None:
        pass

    @abstractmethod
    def fetch(self, document_results: Document) -> FileResponse:
        pass

    @abstractmethod
    def delete(self, document_key_id: Union[UUID, str]) -> None:
        pass
