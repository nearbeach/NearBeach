from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from NearBeach.views.document_views import FILE_HANDLER
from django.conf import settings
from NearBeach.models import (
    Document,
    DocumentPermission,
)

import datetime

User = get_user_model()


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
        self.clean_up_generic_object_documents(self, "kanban_card", "kanban_card_description")
        self.clean_up_generic_object_documents(self, "project", "project_description")
        self.clean_up_generic_object_documents(self, "requirement", "requirement_scope")
        self.clean_up_generic_object_documents(self, "requirement_item", "requirement_item_scope")
        self.clean_up_generic_object_documents(self, "task", "task_long_description")
        self.clean_up_organisation_documents(self)
        self.clean_up_rfc_documents(self)

    @staticmethod
    def get_today():
        return datetime.datetime.today()

    @staticmethod
    def purge_document_from_blob(_, document_key_id):
        FILE_HANDLER.delete(document_key_id=document_key_id)

    @staticmethod
    def clean_up_generic_object_documents(origin, field, description_field):
        clean_after_days = getattr(settings, "DOCUMENTATION_CLEAN_AFTER_DAYS", 90)
        todays_date = origin.get_today()
        expired_date = todays_date - datetime.timedelta(days=clean_after_days)

        documents_to_be_purged = DocumentPermission.objects.filter(
            is_deleted=True,
            is_purged=False,
            date_modified__gte=expired_date,
            **{F"{field}__isnull": False},
        )

        # Loop through all the records - and make sure the document is not in the description
        purged_document_keys = []
        for single_document in documents_to_be_purged:
            document_key_id = str(single_document.document_key_id)
            single_object = getattr(single_document, field)
            description = getattr(single_object, description_field)

            if document_key_id not in description:
                # Process deleting the file
                origin.purge_document_from_blob(document_key_id)

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

    @staticmethod
    def clean_up_organisation_documents(origin):
        clean_after_days = getattr(settings, "DOCUMENTATION_CLEAN_AFTER_DAYS", 90)
        todays_date = origin.get_today()
        expired_date = todays_date - datetime.timedelta(days=clean_after_days)

        documents_to_be_purged = DocumentPermission.objects.filter(
            is_deleted=True,
            is_purged=False,
            date_modified__gte=expired_date,
            organisation__isnull=False,
        )

        # Loop through all the records - and make sure the document is not in the description
        for single_document in documents_to_be_purged:
            document_key_id = str(single_document.document_key_id)
            origin.purge_document_from_blob(document_key_id)

        # Bulk update to purged documents
        Document.objects.filter(
            document_key__in=documents_to_be_purged.values("document_key"),
        ).update(
            is_purged=True,
            date_modified=todays_date,
        )

        DocumentPermission.objects.filter(
            document_key__in=documents_to_be_purged.values("document_key"),
        ).update(
            is_purged=True,
            date_modified=todays_date,
        )

    @staticmethod
    def clean_up_rfc_documents(self):
        clean_after_days = getattr(settings, "DOCUMENTATION_CLEAN_AFTER_DAYS", 90)
        todays_date = self.get_today()
        expired_date = todays_date - datetime.timedelta(days=clean_after_days)

        documents_to_be_purged = DocumentPermission.objects.filter(
            is_deleted=True,
            is_purged=False,
            date_modified__gte=expired_date,
            request_for_change__isnull=False,
        )

        # Loop through all the records - and make sure the document is not in the description
        purged_document_keys = []
        for single_document in documents_to_be_purged:
            document_key_id = str(single_document.document_key_id)
            single_object = single_document.request_for_change

            rfc_summary = single_object.rfc_summary
            rfc_risk_and_impact_analysis = single_object.rfc_risk_and_impact_analysis
            rfc_implementation_plan = single_object.rfc_implementation_plan
            rfc_backout_plan = single_object.rfc_backout_plan
            rfc_test_plan = single_object.rfc_test_plan

            if (document_key_id not in rfc_summary &
                    document_key_id not in rfc_risk_and_impact_analysis &
                    document_key_id not in rfc_implementation_plan &
                    document_key_id not in rfc_backout_plan &
                    document_key_id not in rfc_test_plan
            ):
                # Process deleting the file
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
