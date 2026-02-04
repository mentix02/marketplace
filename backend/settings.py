from sys import argv
from pathlib import Path

from environ import Env

env = Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['*']),
)

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / '.env.local'

if ENV_FILE.is_file():
    env.read_env(ENV_FILE)

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')
IS_TEST = any('test' in arg for arg in argv)

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'djmoney',
    'ordered_model',
    'django_filters',
    'rest_framework',
]

LOCAL_APPS = [
    'apps.user.apps.UserConfig',
    'apps.seller.apps.SellerConfig',
    'apps.product.apps.ProductConfig',
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

if IS_TEST:
    DATABASES = {
        'default': {
            'NAME': ':memory:',
            'ENGINE': 'django.db.backends.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': env.db(),
    }

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {},
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        'OPTIONS': {
            'location': 'static/',
        },
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

PASSWORD_HASHERS = [
    'apps.user.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]

AUTH_USER_MODEL = 'user.User'

INTERNAL_IPS = ['127.0.0.1']

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

# REST Framework Configuration

REST_FRAMEWORK = {
    'PAGE_SIZE': 27,
    'SEARCH_PARAM': 'q',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ALGORITHM': 'RS256',
    'JWK_URL': env('JWK_URL'),
}

# Django Files S3 Storage Configuration

AWS_S3_FILE_OVERWRITE = False
AWS_S3_ADDRESSING_STYLE = 'virtual'
AWS_S3_REGION_NAME = env('AWS_REGION')
AWS_STORAGE_BUCKET_NAME = env('AWS_BUCKET')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
