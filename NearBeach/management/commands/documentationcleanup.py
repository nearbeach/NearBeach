from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Q, F, TextField, Field
from django.db.models.functions import Cast
from NearBeach.views.document_views import FILE_HANDLER

from django.conf import settings

from NearBeach.models import (
    Document,
    DocumentPermission,
)

User = get_user_model()

import datetime
import uuid


class Command(BaseCommand):
    help = "Run this command to remove any deleted documents/files that have been in the system for x amount of months."

    def handle(self, *args, **kwargs):
        """
        Removes all the deleted documents from the blob storage, with some exceptions.

        Method
        1. Find all deleted documents that have not already been purged
        2. Loop through all the documents, and make sure the document is still not located within the object description
        3. Remove document from blob, if it meets the above requirements
        4. Bulk update - tell system we have PURGED the files
        """

        documentation_clean_up = getattr(settings, "DOCUMENTATION_CLEAN_UP", False)
        if not documentation_clean_up:
            print("Documentation Clean Up in the Settings file is set to FALSE. Will not proceed")
            return

        # Clean up happens in two parts
        self.clean_up_kanban_card_documents()
        self.clean_up_organisation_documents() #*
        self.clean_up_project_documents()
        self.clean_up_requirement_documents()
        self.clean_up_requirement_item_documents()
        self.clean_up_rfc_documents() #*
        self.clean_up_task_documents()


    @staticmethod
    def get_today():
        return datetime.datetime.today()

    @staticmethod
    def purge_document_from_blob(self):
        return

    @staticmethod
    def clean_up_kanban_card_documents(self):
        clean_after_days = getattr(settings, "DOCUMENTATION_CLEAN_AFTER_DAYS", 90)
        todays_date = self.get_today()
        expired_date = todays_date - datetime.timedelta(days=clean_after_days)

        documents_to_be_purged = DocumentPermission.objects.filter(
            is_deleted=True,
            is_purged=False,
            date_modified__gte=expired_date,
            kanban_card__isnull=False,
        )

        # Loop through all the records - and make sure the document is not in the description
        purged_document_keys = []
        for single_document in documents_to_be_purged:
            document_key_id = str(single_document.document_key_id)
            description = single_document.kanban_card_description

            if document_key_id not in description:
                #Process deleting the file
                self.purge_document_from_blob(document_key_id)

                purged_document_keys.append(document_key_id)

        # Bulk update to purged documents
        Document.objects.filter(
            document_key__in=purged_document_keys,
        ).update(
            is_purged=True,
            date_modified=todays_date,
        )

        DocumentPermission.objects.filter(
            document_key__in=purged_document_keys,
        ).update(
            is_purged=True,
            date_modified=todays_date,
        )

        return
