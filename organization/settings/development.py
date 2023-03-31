from .base import *
from datetime import timedelta

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=True, cast=bool)


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'attendance_job_portal_db',
        'USER': 'root',
        'PASSWORD': "",
        'HOST': 'localhost',
        'PORT': ''
    }
}

INTERNAL_IPS = '127.0.0.1'

ZOOM_API_KEY = config('ZOOM_API_KEY')
ZOOM_API_SECRET = config('ZOOM_API_SECRET')

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'rfaizan540@gmail.com'
EMAIL_HOST_PASSWORD = 'iqvdhwychtizncdv'
