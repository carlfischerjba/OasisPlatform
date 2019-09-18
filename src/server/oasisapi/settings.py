"""
Django settings for oasisapi project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

from rest_framework.reverse import reverse_lazy

from ...conf import iniconf  # noqa
from ...conf.celeryconf import *  # noqa

IN_TEST = 'test' in sys.argv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = iniconf.settings.get('server', 'debug', fallback=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = iniconf.settings.get('server', 'secret_key', fallback='' if not DEBUG else 'supersecret')

_allowed_hosts = iniconf.settings.get('server', 'allowed_hosts', fallback='')
if _allowed_hosts:
    ALLOWED_HOSTS = _allowed_hosts.split(',')
else:
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_filters',
    'rest_framework',
    'drf_yasg',
    'rest_framework_simplejwt.token_blacklist',

    'src.server.oasisapi.files',
    'src.server.oasisapi.portfolios',
    'src.server.oasisapi.analyses',
    'src.server.oasisapi.analysis_models',
    'src.server.oasisapi.data_files',
    'src.server.oasisapi.healthcheck',
    'src.server.oasisapi.oed_info',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'src.server.oasisapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'src.server.oasisapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DB_ENGINE = iniconf.settings.get('server', 'db_engine', fallback='django.db.backends.sqlite3')

if DB_ENGINE == 'django.db.backends.sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': os.path.join(BASE_DIR, iniconf.settings.get('server', 'db_name', fallback='db.sqlite3')),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': iniconf.settings.get('server', 'db_name'),
            'HOST': iniconf.settings.get('server', 'db_host'),
            'PORT': iniconf.settings.get('server', 'db_port'),
            'USER': iniconf.settings.get('server', 'db_user'),
            'PASSWORD': iniconf.settings.get('server', 'db_pass'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []
AUTHENTICATION_BACKENDS = iniconf.settings.get('server', 'auth_backends', fallback='django.contrib.auth.backends.ModelBackend').split(',')


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = iniconf.settings.get('server', 'media_root', fallback=os.path.join(BASE_DIR, 'media'))

# https://github.com/davesque/django-rest-framework-simplejwt
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  iniconf.settings.get_timedelta('server', 'TOKEN_ACCESS_LIFETIME', fallback='hours=1'),
    'REFRESH_TOKEN_LIFETIME': iniconf.settings.get_timedelta('server', 'TOKEN_REFRESH_LIFETIME', fallback='days=2'),
    'ROTATE_REFRESH_TOKENS': iniconf.settings.getboolean('server', 'TOKEN_REFRESH_ROTATE', fallback=True),
    'BLACKLIST_AFTER_ROTATION': iniconf.settings.getboolean('server', 'TOKEN_REFRESH_ROTATE', fallback=True),
    'SIGNING_KEY': iniconf.settings.get('server', 'token_sigining_key', fallback=SECRET_KEY),
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'src.server.oasisapi.filters.Backend',
    ),
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S.%fZ',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
}


if IN_TEST:
    BROKER_URL = 'memory://'
    LOGGING['root'] = {}


SWAGGER_SETTINGS = {
    'DEFAULT_INFO': 'src.server.oasisapi.urls.api_info',
    'LOGIN_URL': reverse_lazy('rest_framework:login'),
    'LOGOUT_URL': reverse_lazy('rest_framework:logout'),
}
