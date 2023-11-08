"""
Django settings for root project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from os.path import join
from environ import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# https://django-environ.readthedocs.io/en/latest/

env = Env()
env.read_env('.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    'SECRET_KEY', default='django-insecure-v@h$!bry(=s(l9k+6pmk2urzug(8u_yot!=in^m^afje+&t1q8'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'root.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD')
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#specifying-custom-user-model

AUTH_USER_MODEL = 'main.User'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'root.utils.exceptions.exception_handler',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detail': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}\n'+f'{"*"*30}\n',
            'style': '{',
        },
        'info_format': {
            'format': '{asctime} {message}',
            'style': '{',
        }
    },
    'filters': {
        'error_only_filter': {
            '()': 'root.utils.logging.ErrorOnlyFilter'
        },
        'cron_error_filter': {
            '()': 'root.utils.logging.CronErrorFilter'
        },
        'warning_only_filter': {
            '()': 'root.utils.logging.WarningOnlyFilter'
        },
        'critical_only_filter': {
            '()': 'root.utils.logging.CriticalOnlyFilter'
        },
        'info_only_filter': {
            '()': 'root.utils.logging.InfoOnlyFilter'
        }
    },
    'handlers': {
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'detail',
            'filename': join(BASE_DIR, 'logs/errors.log'),
            'filters': {'error_only_filter', }
        },
        'cron_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'detail',
            'filename': join(BASE_DIR, 'logs/cron.log'),
            'filters': {'cron_error_filter', }
        },
        'warning': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'detail',
            'filename': join(BASE_DIR, 'logs/warning.log'),
            'filters': {'warning_only_filter', }
        },
        'critical': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'formatter': 'detail',
            'filename': join(BASE_DIR, 'logs/critical.log'),
            'filters': {'critical_only_filter', }
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'info_format',
            'filename': join(BASE_DIR, 'logs/info.log'),
            'filters': {'info_only_filter', }
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': {'cron_error', 'error', 'warning', 'critical', 'info'}
    }
}
