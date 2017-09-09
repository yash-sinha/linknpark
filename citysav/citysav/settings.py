"""
Django settings for citysav project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=vasc()+7h#j2965j81f$m*268yesn1szq^&nr&j%9+0av5+k3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

HOME_DIR = '/home/citysavior/'
CERT_DIR = '/home/citysavior/cert/'


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts',
    'rest_framework',
    'push_notifications',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'citysav.urls'

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

WSGI_APPLICATION = 'citysav.wsgi.application'

PUSH_NOTIFICATIONS_SETTINGS = {
        'FCM_API_KEY':'AAAAtYB8t5g:APA91bFGSmI2_tOKo4ed19y5xjpUfZlY17SyJgt8Dv0SXhp6hq-F4-IbqN_PemTyH5Rk70Sm7VLeT-XfkTm3fCeHHAvyKsHTgRQ4y_reAmd6Ec9U7Azi6HT8YyG7uaSBiBkfgatwc-90',
        "APNS_CERTIFICATE": os.path.join(CERT_DIR, "PushCertProd3pem.pem"),
        "APNS_TOPIC": "co.citySavior",
        "APNS_USE_SANDBOX": False,

    }
#


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'citysavior$default',
        'HOST':'citysavior.mysql.pythonanywhere-services.com',
        'USERNAME': 'citysavior',
        'PASSWORD': 'citysavmysql',
        'OPTIONS':{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT ='/home/citysavior/static/'

MEDIA_URL ='/media/'
MEDIA_ROOT = '/home/citysavior/media/'
IMAGE_UPLOAD_DIR = 'uploads/'
IMAGE_THUMBNAIL_DIR='thumbnails/'
CORS_ORIGIN_ALLOW_ALL = True

EMAIL_USE_TLS =True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_PASSWORD = 'citysav101'
EMAIL_HOST_USER = 'citysavior1@gmail.com'
EMAIL_PORT =587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER



