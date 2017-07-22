"""
Django settings for siscon project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
# Django settings for siscon project.
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))



# from unipath import Path
# BASE_DIR = Path(__file__).ancestor(2)

DEBUG = True

# ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', 'localhost']

ALLOWED_HOSTS = ['*']

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('carr', 'carrm29@yahoo.com.mx'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'siscon.db',  # Or path to database file if using sqlite3.
        'USER': '',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
# TIME_ZONE = 'America/Mexico'

TIME_ZONE = 'America/Mexico_City'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-MX'

# Si se Borra el SITE en admin, puede maracar error, al dar otro te  da el siguiente
# ID que debe ser colocado aqui para que no de error, es mejor actualizarlo
# para que no genere otro ID y se tenga que modificar esta linea.

SITE_ID = 2

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

DATE_INPUT_FORMATS = ('%d-%m-%Y',)

# If you set this to False, Django will not use timezone-aware datetimes.
#Una vez cambiado este parametro a False las fechas que se almacenan en Django
# y las que se encuentran fisicamente en la base de datos son las mismas.
USE_TZ = False


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''  # BASE_DIR.child('media')
# aca se guardaran todas la fotos que suvamos en ste proyecto no
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'


# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    # BASE_DIR.child('static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
 #   'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = '%_3s2r!t#hg9n6sq0^4q!&amp;rbr$nma+hlw8*vzy(83@98@oxnns'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'siscon.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'siscon.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    # BASE_DIR.child('templates'),
)

INSTALLED_APPS = (
    'apps.apps.AppAppsConfig',
    'apps.inicio',
    'apps.registros',
    'apps.menu',
    'apps.usuarios',
    'apps.notas',
    'apps.pvrep',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'social.apps.django_app.default',
    'social_django',
    'import_export',
)


IMPORT_EXPORT_USE_TRANSACTIONS = True


from django.core.urlresolvers import reverse_lazy

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('menu')
LOGOUT_URL = reverse_lazy('logout')
# LOGIN_URL = '/'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/menu'

SOCIAL_AUTH_TWITTER_KEY = 'zP1pu2Rzzl6BXlgdRvu8OdSFw'
SOCIAL_AUTH_TWITTER_SECRET = 'cul1Ov337BR8s8IN09qUiB7jb8lvRDckpIya64n8eOQO1Mn5wT'

SOCIAL_AUTH_FACEBOOK_KEY = '591882320949570'
SOCIAL_AUTH_FACEBOOK_SECRET = 'c4e3805f07943ae9cc5d1e2f6581335d'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

# Variables para enviar un mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'comercialccsys@gmail.com'
EMAIL_HOST_PASSWORD = 'comerABC123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'comercialccsys@gmail.com'

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)

#DATABASES['default'].update(db_from_env)

#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')


#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')