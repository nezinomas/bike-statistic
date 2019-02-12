from .base import *


# ================   DEBUG CONFIGURATION
DEBUG = False
TEMPLATE_DEBUG = DEBUG


# ================   project CONFIGURATION
ALLOWED_HOSTS = ['*']


# ================   APP CONFIGURATION
INSTALLED_APPS += [
    'django_crontab',
]


# ================   CRONJOBS
CRONJOBS = [
    ('2,30 * * * *', 'project.reports.cron.insert_from_endomondo', '> /dev/null 2>&1'),
]
