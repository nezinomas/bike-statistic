from .base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG


ALLOWED_HOSTS = ENV.list("ALLOWED_HOSTS")


INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]


SHELL_PLUS_PRINT_SQL = True


STATIC_ROOT = None
STATICFILES_DIRS = [
    os.path.join(SITE_ROOT, 'static'),
]


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE


# Overwriten TEMPLATE OPTION
# disabled template cashing
TEMPLATES[0]['OPTIONS']['loaders'] = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader', ]


INTERNAL_IPS = ['127.0.0.1', 'localhost']


DEBUG_TOOLBAR_PATCH_SETTINGS = False
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
