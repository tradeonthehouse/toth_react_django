"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os, environ
from pathlib import Path

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='insecure-S#perS3crEt_007')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

try:
    # expects 1 or 0
    DEBUG = int(os.environ.get("DEBUG", default=0))
except:
    DEBUG = False

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS", default="*").split(" ")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "api",
    "api.user",
    "api.authentication",
    "monthlymodel"
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'frontend/build')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE"  : "django.db.backends.postgresql",
        "NAME"    : "defaultdb",
        "USER"    : "doadmin",
        "PASSWORD": "AVNS_BXQjSO7uCq-TYI_hpcE",
        "HOST"    : "db-postgresql-blr1-41046-do-user-13753354-0.b.db.ondigitalocean.com",
        "PORT"    : 25060,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user Model
AUTH_USER_MODEL = "api_user.User"

# ##################################################################### #
# ################### REST FRAMEWORK             ###################### #
# ##################################################################### #

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "api.authentication.backends.ActiveSessionAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

# ##################################################################### #
#  CORS 
# ##################################################################### #

CORS_ALLOW_ALL_ORIGINS=True

# Load the default ones
CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000", "https://orca-app-zlgcl.ondigitalocean.app:8080"]

# Leaded from Environment
CORS_ALLOWED_ORIGINS_ENV = env("CORS_ALLOWED_ORIGINS", default=None)

if CORS_ALLOWED_ORIGINS_ENV:
    CORS_ALLOWED_ORIGINS += CORS_ALLOWED_ORIGINS_ENV.split(' ')
    
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
  


# ##################################################################### #
#  TESTING 
# ##################################################################### #

TESTING = False
TEST_RUNNER = "core.test_runner.CoreTestRunner"
