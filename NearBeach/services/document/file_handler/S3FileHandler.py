import boto3
from botocore.config import Config

from NearBeach.services.document.file_handler.FileHandler import FileHandler
from django.http import FileResponse


class S3FileHandler(FileHandler):
    def __init__(self, local_settings):
        boto_init_values = {
            "aws_access_key_id": local_settings.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": local_settings.AWS_SECRET_ACCESS_KEY,
        }
        if getattr(local_settings, "AWS_S3_ENDPOINT_URL", None):
            # Assume the person is using minio so defaults are the values
            # that will allow for connection to minio
            boto_init_values.update(
                endpoint_url=local_settings.AWS_S3_ENDPOINT_URL,
                aws_session_token=getattr(local_settings, "AWS_S3_SESSION_TOKEN", None),
                config=getattr(
                    local_settings,
                    "AWS_CONFIG",
                    boto3.session.Config(signature_version='s3v4'),
                ),
                verify=getattr(local_settings, "AWS_VERIFY_TLS", True),
                **getattr(local_settings, "AWS_INIT_VALUES", {})
            )
            # Log any issues for the user
            self._connect_check_client_s3(boto_init_values=boto_init_values)

        self._s3 = boto3.client("s3",   **boto_init_values)
        self._bucket = local_settings.AWS_STORAGE_BUCKET_NAME

    @staticmethod
    def _connect_check_client_s3(boto_init_values):
        config = Config(
            connect_timeout=4,
            retries=dict(
                max_attempts=1,
            )
        )
        boto_init_values.update(
            config=config
        )
        client = boto3.client("s3", **boto_init_values)

        # Check to see if the connection works
        try:
            client.list_buckets()
        except Exception as e:
            print(F"An issue has occurred trying to connect to the S3 bucket. Please see the following errors - {e}")

    def delete(self, document_key_id):
        # Use boto3 to delete
        objects_to_delete = self._s3.list_objects(
            Bucket=self._bucket,
            Prefix=F"private/{document_key_id}"
        )

        delete_keys = {
            'Objects': [
                {'Key': k} for k in [obj['Key'] for obj in objects_to_delete.get('Contents', [])]
            ]
        }

        self._s3.delete_objects(
            Bucket=self._bucket,
            Delete=delete_keys
        )

    def fetch(self, document_results):
        # Use boto3 to download
        response = self._s3.get_object(
            Bucket=self._bucket,
            Key=str(document_results.document),
        )
        return FileResponse(
            response["Body"],
            as_attachment=True,
            filename=document_results.document_description,
        )

    def upload(self, upload_document, document_results, file):
        # Use boto to upload the file
        # Upload a new file
        self._s3.upload_fileobj(
            file,
            self._bucket,
            str(document_results.document),
        )