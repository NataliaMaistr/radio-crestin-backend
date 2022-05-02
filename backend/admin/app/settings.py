"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

import dj_database_url
import tablib
from import_export.formats import base_formats
from import_export.formats.base_formats import DEFAULT_FORMATS, CSV

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('ADMIN_SECRET_KEY', 'sdg43gsdgsdgsg#S$#GFDFTFUYAFUYDGJGH')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('ADMIN_DEBUG', 'false').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ADMIN_ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS += ['127.0.0.1', ]
if DEBUG:
    print('ALLOWED_HOSTS:', ALLOWED_HOSTS)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'collectfast',
    'django.contrib.staticfiles',
    'django_filters',
    'import_export',
    'storages',
    'django_dumpdata_one',
    'web',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Bucharest'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# CORS
CORS_ORIGIN_WHITELIST = os.environ.get('ADMIN_CORS_ORIGIN_WHITELIST', '').split(',')

CSRF_TRUSTED_ORIGINS = os.environ.get('ADMIN_CORS_ORIGIN_WHITELIST', '').split(',')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get('ADMIN_STATIC_ROOT', 'static_data'))
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

# Database
CONN_MAX_AGE = 0
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
if 'ADMIN_DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(env='ADMIN_DATABASE_URL', conn_max_age=CONN_MAX_AGE),
    }
else:
    print("Warning! No ADMIN_DATABASE_URL!")

# Logging
DEFAULT_HANDLERS = ['console']
if DEBUG:
    DEFAULT_HANDLERS = ['console']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.utils.autoreload': {
            'level': 'INFO',
        },
        '': {
            'handlers': DEFAULT_HANDLERS,
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': DEFAULT_HANDLERS,
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# IMPORT EXPORT
IMPORT_EXPORT_USE_TRANSACTIONS = True
IMPORT_EXPORT_CHUNK_SIZE = 1000


class NUMBERS_CSV(base_formats.CSV):
    def get_title(self):
        return "csv - Apple Numbers, using semicolon"

    def create_dataset(self, in_stream, **kwargs):
        kwargs['delimiter'] = ';'
        kwargs['quotechar'] = '"'
        kwargs['format'] = 'csv'
        return tablib.import_set(in_stream, **kwargs)

    def export_data(self, dataset, **kwargs):
        kwargs['delimiter'] = ';'
        kwargs['quotechar'] = '"'
        kwargs['format'] = 'csv'
        return dataset.export(**kwargs)


class EXCEL_CSV(NUMBERS_CSV):
    def get_title(self):
        return "csv - Excel, using semicolon"


class SIMPLE_COMMA_CSV(base_formats.CSV):
    def get_title(self):
        return "csv - using simple comma"

    def create_dataset(self, in_stream, **kwargs):
        kwargs['delimiter'] = ','
        kwargs['quotechar'] = '"'
        kwargs['format'] = 'csv'
        return tablib.import_set(in_stream, **kwargs)

    def export_data(self, dataset, **kwargs):
        kwargs['delimiter'] = ','
        kwargs['quotechar'] = '"'
        kwargs['format'] = 'csv'
        return dataset.export(**kwargs)


DEFAULT_FORMATS.remove(CSV)
DEFAULT_FORMATS.insert(0, NUMBERS_CSV)
DEFAULT_FORMATS.insert(1, EXCEL_CSV)
DEFAULT_FORMATS.insert(2, SIMPLE_COMMA_CSV)

# AWS settings
AWS_ACCESS_KEY_ID = os.environ.get('ADMIN_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('ADMIN_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('ADMIN_AWS_STORAGE_BUCKET_NAME')

AWS_S3_REGION_NAME = "eu-central-1"
AWS_S3_CUSTOM_DOMAIN = os.environ.get('ADMIN_AWS_S3_CUSTOM_DOMAIN', 'cdn.radio-crestin.com')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False

AWS_STATIC_LOCATION = 'media/static'
STATICFILES_STORAGE = 'web.storage_backends.StaticStorage'
COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
AWS_PRELOAD_METADATA = True
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
DEFAULT_FILE_STORAGE = 'web.storage_backends.PublicMediaStorage'

AWS_PRIVATE_MEDIA_LOCATION = 'media/private'
PRIVATE_FILE_STORAGE = 'web.storage_backends.PrivateMediaStorage'
