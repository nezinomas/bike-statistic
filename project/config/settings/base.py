import os
from ..secrets import get_secret

AUTH_USER_MODEL = 'users.User'

# ================   PATH CONFIGURATION
# ..\project_project\project\config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ..\project_project\project
SITE_ROOT = os.path.dirname(BASE_DIR)
# ..\project_project
PROJECT_ROOT = os.path.dirname(SITE_ROOT)


# ================   SITE CONFIGURATION
LOGOUT_REDIRECT_URL = 'reports:index'
LOGIN_REDIRECT_URL = 'reports:index'
LOGIN_URL = 'users:login'


# ================   CASH CONFIGURATION
CASH_ROOT = os.path.join(PROJECT_ROOT, 'cash')


# ================   MEDIA CONFIGURATION
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')
MEDIA_URL = "/media/"


# ================   STATIC FILE CONFIGURATION
STATIC_URL = '/static/'
STATICFILES_DIRS = os.path.join(SITE_ROOT, 'static')


# ================   DEBUG CONFIGURATION
DEBUG = False
TEMPLATE_DEBUG = DEBUG


# ================   SECRET CONFIGURATION
SECRET_KEY = get_secret("SECRET_KEY")


# ================   project CONFIGURATION
ALLOWED_HOSTS = ['*']


# ================   DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(PROJECT_ROOT, '_config_db.cnf'),
        },
    }
}


# ================   GENERAL CONFIGURATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

USE_THOUSAND_SEPARATOR = True


# ================   TEMPLATE CONFIGURATION
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SITE_ROOT, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'project.bikes.context.bike_list',
                'project.bikes.context.component_list',
                'project.goals.context.goal_list',
            ],
        },
    },
]


# ================   MIDDLEWARE CONFIGURATION
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ================   APP CONFIGURATION
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'bootstrap_datepicker_plus',
    'crispy_forms',
    'bootstrap4',
    'widget_tweaks',
    'crequest',
    'project.core',
    'project.bikes',
    'project.goals',
    'project.reports',
    'project.users'
]


# ================   URL CONFIGURATION
ROOT_URLCONF = 'project.config.urls'


# ================   WSGI CONFIGURATION
WSGI_APPLICATION = 'project.config.wsgi.application'


# ================   PASSWORD VALIDATORS CONFIGURATION
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


# ================   CRISPY FORMS
CRISPY_TEMPLATE_PACK = 'bootstrap4'
