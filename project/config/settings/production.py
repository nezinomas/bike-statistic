from .base import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['bike.unknownbug.net']

INSTALLED_APPS += [
    'django_crontab',
]

TEMPLATES[0]['OPTIONS']['loaders'] = [
    ['django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader', ],
     ],
]

SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'


CRONJOBS = [
    ('2,30 * * * *', 'project.reports.cron.cron_insert_from_garmin', '> /dev/null 2>&1'),
]
