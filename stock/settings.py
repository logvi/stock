"""
Django settings for stock project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*e^p-5dbk911%#kz)k(ttbreb+b6u8tu@0^mt1dhel&iku#8yg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

location = lambda *path: os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "..", "..", *path)

ALLOWED_HOSTS = []

STATIC_ROOT = location("public/static/")

STATIC_URL = "/static/"

STATICFILES_DIRS = (
    location("stock/static"),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stock',
    'apps.AppStock',
    'south',
    'debug_toolbar'
)
    # 'south',
    # 'debug_toolbar'

INTERNAL_IPS = ("127.0.0.1",)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'stock.urls'

WSGI_APPLICATION = 'stock.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'stock',
    'USER': 'postgres',
    'PASSWORD': 'postgres',
    'HOST': '', # Set to empty string for localhost.
    'PORT': '5432', # Set to empty string for default.
    }
}

TEMPLATE_LOADERS = (
    ("django.template.loaders.cached.Loader", (
        "django.template.loaders.filesystem.Loader",
        "django.template.loaders.app_directories.Loader",
    )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = '/stock/'
LOGOUT_REDIRECT_URL = '/stock/'

try:
    from stock.settings_prod import *
except ImportError:
    pass

try:
    from settings_local import *
except ImportError:
    pass