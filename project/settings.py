"""
Django settings for SCRPR project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import django_heroku
import os
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', default='e3950e11bf81cccb010c3c7ca6b7cc729aaaf0947a588edefe145f172847770959cde1194c553e05b1d1c2abdb0d5f4b84201decd57415e66f5e5b6e7419a415')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ['127.0.0.1',]

# frontend will be working from port 3000
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('SENDGRID_SMTP_SERVER')
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('SENDGRID_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_SMTP_PASSWORD')
EMAIL_USE_TLS = True
OWN_EMAIL = os.environ.get('OWN_EMAIL')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

LOGIN_REDIRECT_URL = '/'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django_crontab',
    'debug_toolbar',
    'tinymce',
    'scrpr',
    'web_scraper',
    'authentication',
    'smart_emails'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

AUTH_USER_MODEL = 'authentication.User'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'),]
from django.utils.translation import gettext_lazy as _
LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_STORAGE = 'whitenoise.django.CompressedManifestStaticFilesStorage'


# Miscellaneous

try:
    from .local_settings import *
except ImportError:
    pass

print(f'Debug: {DEBUG}')

DIRECT_URL = ''

CRONJOBS = [
    (
        '0 */6 * * *',
        'django.core.management.call_command',
        ['updatescrapeddata'],
        f'>> {os.path.join(BASE_DIR, "web_scraper/web_scraping/web_scraping.log")}'
    ),
    (
        '0 12 * * *',
        'smart_emails.cron_daily.send_suggestions'
    ),
    (
        '0 12 * * 1',
        'smart_emails.cron_weekly.send_suggestions'
    ),
    (
        '0 12 1 * *',
        'smart_emails.cron_monthly.send_suggestions'
    )
]

# TinyMCE settings

TINYMCE_DEFAULT_CONFIG = {
    'language': 'en',
    'theme': "advanced",
    'relative_urls': False,
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    'theme_advanced_statusbar_location': "bottom",
    'theme_advanced_resizing': True,
    'element_format': "html",
    'plugins' : "autolink,lists,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",
    'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,bullist,numlist,sub,sup,|,forecolor,backcolor,formatselect,fontsizeselect",
    'theme_advanced_buttons2' : "outdent,indent,|,undo,redo,|,link,unlink,anchor,image,tablecontrols,removeformat,code",
    'theme_advanced_buttons3_add' : "tablecontrols",
    'table_styles' : "Header 1=header1;Header 2=header2;Header 3=header3",
    'table_cell_styles' : "Header 1=header1;Header 2=header2;Header 3=header3;Table Cell=tableCel1",
    'table_row_styles' : "Header 1=header1;Header 2=header2;Header 3=header3;Table Row=tableRow1",
    'table_cell_limit' : 100,
    'table_row_limit' : 5,
    'table_col_limit' : 5,
    'table_inline_editing': True,
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True


# Cache settings

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'scraping_cache_table',
        'TIMEOUT': 1200,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}


# adapt paths for deployment on Heroku
django_heroku.settings(locals())
