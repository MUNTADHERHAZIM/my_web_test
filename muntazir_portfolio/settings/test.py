"""Test settings for the project."""

from .base import *

# Test database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable migrations for faster tests
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Test cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Disable Redis for tests
REDIS_URL = None

# Test email backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Disable Celery for tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Test media settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')

# Disable logging during tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['null'],
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['null'],
            'propagate': False,
        },
    }
}

# Test security settings
SECRET_KEY = 'test-secret-key-not-for-production'
DEBUG = True
ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']

# Disable CSRF for tests
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Test static files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Disable compression for tests
COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

# Test internationalization
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Password validation (simplified for tests)
AUTH_PASSWORD_VALIDATORS = []

# Test file upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024  # 1MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024  # 1MB

# Test session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Disable security middleware for tests
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_BROWSER_XSS_FILTER = False

# Test-specific apps
INSTALLED_APPS += [
    'django_extensions',
]

# Test middleware (minimal)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Test template settings
TEMPLATES[0]['OPTIONS']['debug'] = True

# Disable external services for tests
RECAPTCHA_PUBLIC_KEY = 'test-public-key'
RECAPTCHA_PRIVATE_KEY = 'test-private-key'
RECAPTCHA_USE_SSL = False

# Test search settings
if 'haystack' in INSTALLED_APPS:
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }

# Test analytics (disabled)
GOOGLE_ANALYTICS_ID = None
GOOGLE_TAG_MANAGER_ID = None

# Test social auth (disabled)
SOCIAL_AUTH_GITHUB_KEY = 'test-github-key'
SOCIAL_AUTH_GITHUB_SECRET = 'test-github-secret'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'test-google-key'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'test-google-secret'

# Test storage settings
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Test thumbnail settings
if 'easy_thumbnails' in INSTALLED_APPS:
    THUMBNAIL_DEBUG = True
    THUMBNAIL_BACKEND = 'easy_thumbnails.backends.default.DefaultBackend'
    THUMBNAIL_KEY_PREFIX = 'test-thumbnails'

# Test pagination
PAGINATE_BY = 5  # Smaller for tests

# Test rate limiting (disabled)
if 'django_ratelimit' in INSTALLED_APPS:
    RATELIMIT_ENABLE = False

# Test monitoring (disabled)
SENTRY_DSN = None

# Test performance settings
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: False,
}

# Test fixture settings
FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures'),
    os.path.join(BASE_DIR, 'tests', 'fixtures'),
]

# Test custom settings
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
TEST_NON_SERIALIZED_APPS = ['contenttypes', 'auth']

# Disable whitenoise for tests
if 'whitenoise.middleware.WhiteNoiseMiddleware' in MIDDLEWARE:
    MIDDLEWARE.remove('whitenoise.middleware.WhiteNoiseMiddleware')

# Test CORS settings (if applicable)
if 'corsheaders' in INSTALLED_APPS:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True

# Test REST framework settings (if applicable)
if 'rest_framework' in INSTALLED_APPS:
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    }

# Test GraphQL settings (if applicable)
if 'graphene_django' in INSTALLED_APPS:
    GRAPHENE = {
        'SCHEMA': 'config.schema.schema',
        'MIDDLEWARE': [],
    }

print("Test settings loaded successfully")