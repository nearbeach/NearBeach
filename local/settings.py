"""
Django Settings for TESTING PURPOSES

Do not utilise this settings.py file for your own project. Even if it is not
a production environment.

This file is only for the automatic testing and is not build for server use.
"""

import os
from NearBeach import __version__ as VERSION

from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING = {}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jz0k8%ecl#k!z+(9+5(^do1w!11ysus21m41m@i9c#u)*vk($o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '0.0.0.0', '192.168.1.105']


# Application definition

INSTALLED_APPS = [
    'NearBeach.apps.NearBeachConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ROOT_URLCONF = 'NearBeach.urls'
ROOT_URLCONF = 'local.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'NearBeach.context_processors.django_version',
                'NearBeach.context_processors.nearbeach_version',
            ],
        },
    },
]


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PRIVATE_MEDIA_ROOT = os.path.join(PROJECT_PATH, 'private')
PRIVATE_MEDIA_SERVER = 'DefaultServer'
PRIVATE_MEDIA_URL = '/private/'

# Static files setup
# Check to see if we are importing Azure Credentials
if "CLOUDFLARE_ACCOUNT_ID" in os.environ:
    # Get the cloudflare account id
    CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")

    # Setup the variables for the django-storages
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_REGION_NAME = 'auto'
    AWS_LOCATION = F"{VERSION}"
    AWS_S3_ENDPOINT_URL = F"https://{CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com"

    # To use a selfsigned cert you can put the path to the cert bundle
    # here e.g. AWS_VERIFY_TLS = path/to/cert/bundle.pem
    # AWS_VERIFY_TLS = False

    # AWS_CONFIG can be used to set configure the botocore config
    # see https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html


    # Defining STORAGES
    STORAGES = {"staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"}}

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


# Check to see if we are importing AWS credentials
if "AWS_ACCESS_KEY_ID" in os.environ and "CLOUDFLARE_ACCOUNT_ID" not in os.environ:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")

# Check to see if we are importing Azure Credentials
if "AZURE_STORAGE_CONNECTION_STRING" in os.environ:
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MAX_FILE_SIZE_UPLOAD = 104857600
if "MAX_FILE_SIZE_UPLOAD" in os.environ:
    MAX_FILE_SIZE_UPLOAD = os.getenv("MAX_FILE_SIZE_UPLOAD")

# If user wants to use a custom auth user model
# Requested in Issue-533
if "OVERRIDE_AUTH_USER_MODEL" in os.environ:
    AUTH_USER_MODEL = os.getenv("OVERRIDE_AUTH_USER_MODEL")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('SMTP_EMAIL_HOST')
EMAIL_PORT = os.getenv('SMTP_EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('SMTP_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('SMTP_EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
