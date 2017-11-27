# Django settings for smartDNA project.
import os
import sys
import logging
import json
#from django.conf import settings
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
AUTO_LOGOUT_DELAY = 30

ALLOWED_HOSTS = ['DEPLOYMENT_HOST']
DEMO_MODE=False
DEBUG = False
TEMPLATE_DEBUG = DEBUG
WINDOWS=False
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_USE_SSL = True
#EMAIL_USE_TLS = True
PROJECT_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]
def getJSON():
    # Reading JSON data
    #print os.path.dirname((os.path.realpath(__file__))).split("smartDNA")[0]
    with open(PROJECT_PATH+'smartDNA/media/settings.json', 'r') as f:
     json_data = json.load(f)
    print json_data['email_host']
    return json_data

json_data=getJSON()

EMAIL_HOST = json_data['email_host']
EMAIL_PORT = int(json_data['email_port'])
EMAIL_HOST_USER = json_data['email_username']
EMAIL_HOST_PASSWORD = json_data['email_password']
DEFAULT_FROM_EMAIL = 'support@linksmartdna.com'
DEFAULT_TO_EMAIL = 'support@linksmartdna.com'

ADMINS = (
    ('Linksmart Admin', 'support@linksmartdna.com'),
)

#SESSION_COOKIE_DOMAIN="http://ec2-54-69-199-89.us-west-2.compute.amazonaws.com:8001"
SESSION_COOKIE_NAME = 'site2'
#SESSION_COOKIE_PATH =':/tmp'
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'DATABASE_NAME',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'DATABASE_PASSWORD',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia,.org/wiki/List_of_tz_zones_by_nam,e
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Calcutta'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
if WINDOWS:
  MEDIA_ROOT = ('%s/media/' % (os.path.dirname(__file__))) #'D:/smartDNA/media/'
else:
  MEDIA_ROOT = ('%s/media/' % (os.path.dirname(__file__))) #'/home/smartdna/server/smartDNA/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
if WINDOWS:
  STATIC_ROOT = ('%s/static/' % (os.path.dirname(__file__))) #'D:/smartDNA/static/'
else:
  STATIC_ROOT = ('%s/static/' % (os.path.dirname(__file__))) #'/home/smartdna/server/smartDNA/static/'

 # STATIC_ROOT = '/home/smartdna/server/smartDNA/static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = '127(q1m!d)k0n)gdq$1d^e4p7%n*3gsbb0waubmuftw)*9lt__'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)
MIDDLEWARE_CLASSES = (
    'smartDNA.multiPort.MultiPortMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'core.trackware.UserLocationLoggerMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'smartDNA.aloware.AutoLogout',
    )

ROOT_URLCONF = 'smartDNA.urls'

if WINDOWS:
  TEMPLATE_DIRS = ('%s/templates' % (os.path.dirname(__file__)),) #('D:/smartDNA/templates',)
else:
  TEMPLATE_DIRS = ('%s/templates' % (os.path.dirname(__file__)),) #('/home/smartdna/server/smartDNA/templates',)

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.coreConfig',
    'smartdna.apps.smartdnaConfig',
    'googlecharts',
    'pagination',
)

ADMIN_REORDER = (("core", ("Deployment","Logger")),)

# Django Suit configuration example

SUIT_CONFIG = {

    # header

     'ADMIN_NAME': 'SITE_TITLE',

     'HEADER_DATE_FORMAT': 'l, j. F Y',

     'HEADER_TIME_FORMAT': 'H:i',

    # forms

     'SHOW_REQUIRED_ASTERISK': True,  # Default True

     'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu

     'SEARCH_URL': '/admin/auth/user/',

     'MENU_ICONS': {

        'sites': 'icon-leaf',

        'auth': 'icon-lock',

     },

     'MENU_OPEN_FIRST_CHILD': True, # Default True

     'MENU_EXCLUDE': ('auth.group',),

     'MENU': (

	 {'app': 'core', 'icon':'icon-globe', 'models': ('CustomUser','Deployment','Logger','Configuration')},
	 #{'app': 'smartdna', 'icon':'icon-globe', 'models': ('Scan Alert','Scan Monitoring')},
	 {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
	 #{'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
         #{'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
	 #{'label': 'Analytics', 'icon':'icon-picture', 'url': '/analytics/'},
	 #{'label': 'Scan-Monitoring', 'icon':'icon-eye-close', 'url': '/scan_monitoring/'},
         {'label': 'Export Data', 'icon':'icon-briefcase', 'url': '/download_databook/'},
         {'label': 'Export Media', 'icon':'icon-briefcase', 'url': '/download_mediabook/'},
         {'label': 'Import Data', 'icon':'icon-edit', 'url': '/update_product_details/'},
	 {'label': 'Batch Report', 'icon':'icon-eye-open', 'url': '/batch_report/'},
	 {'label': 'Verification Trails', 'icon':'icon-eye-open', 'url': '/audit_monitoring/'},
   {'label': 'Registrations', 'icon':'icon-eye-open', 'url': '/registration_monitoring/'},
   {'label': 'Scan Analysis', 'icon':'icon-eye-open', 'url': '/scan_monitoring/'},
     ),



    # misc

     'LIST_PER_PAGE': 30

}

#Max file size allowed for upload
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

#Max data size allowed in request body
#DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

LOGIN_URL = '/admin/'
DEBUG_TOOLBAR_CONFIG = {
                'INTERCEPT_REDIRECTS': False,
                    }

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

AUTH_USER_MODEL = 'core.CustomUser'
AUTH_PROFILE_MODULE = 'core.UserProfile'
GEOIP_PATH = PROJECT_PATH+'smartDNA/'
