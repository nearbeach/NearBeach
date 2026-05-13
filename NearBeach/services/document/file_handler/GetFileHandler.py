from NearBeach.services.document.file_handler.AzureFileHandler import AzureFileHandler
from NearBeach.services.document.file_handler.LocalFileHandler import LocalFileHandler
from NearBeach.services.document.file_handler.S3FileHandler import S3FileHandler

def get_file_handler(local_settings):
    # Handle the document upload
    if getattr(local_settings, "AWS_ACCESS_KEY_ID", None):
        return S3FileHandler(local_settings)
    if getattr(local_settings, "AZURE_STORAGE_CONNECTION_STRING", None):
        return AzureFileHandler(local_settings)
    return LocalFileHandler(local_settings)
