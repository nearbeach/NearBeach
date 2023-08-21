# The following script, will automatically deploy NearBeach's static files to Cloudflare R2

import NearBeach
import argparse
import boto3  # Need to install through PIP

# Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument("account_id", help="The Account Id for the R2")
parser.add_argument("access_key_id", help="The Access Key required for logging in")
parser.add_argument("access_key_secret", help="The Secret Key, required for logging in")
args = parser.parse_args()

# Obtain the current NearBeach version
current_version = NearBeach.__version__

# Access the Cloudflare R2 using Boto
s3 = boto3.resource('s3',
                    endpoint_url='https://<accound_id>.r2.cloudflarestorage.com',
                    aws_access_key_id='<access_key_id>',
                    aws_secret_access_key='<access_key_secret>'
                    )

print('Buckets:')
for bucket in s3.buckets.all():
    print(' - ', bucket.name)

bucket = s3.Bucket('my-bucket-name')

print('Objects:')
for item in bucket.objects.all():
    print(' - ', item.key)

# Upload a new file
data = open('test.jpg', 'rb')
s3.Bucket('my-bucket').put_object(Key='test.jpg', Body=data)
