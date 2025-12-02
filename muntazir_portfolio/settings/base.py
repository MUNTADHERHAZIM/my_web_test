"""Base settings for muntazir_portfolio project."""

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me-in-production')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

THIRD_PARTY_APPS = [
    'markdownx',
    'taggit',
    'crispy_forms',
    'crispy_tailwind',
    'ckeditor',
    'ckeditor_uploader',
]

LOCAL_APPS = [
    'core',
    'blog',
    'accounts',
    'books',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'muntazir_portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'core.context_processors.site_settings',
                'core.context_processors.active_announcements',
            ],
        },
    },
]

WSGI_APPLICATION = 'muntazir_portfolio.wsgi.application'

# Password validation
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
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'en')
TIME_ZONE = os.environ.get('TIME_ZONE', 'Asia/Baghdad')
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('ar', _('Arabic')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Site ID
SITE_ID = 1

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Markdownx
MARKDOWNX_MARKDOWNIFY_FUNCTION = 'markdownx.utils.markdownify'
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    'markdown.extensions.toc',
]

# Taggit
TAGGIT_CASE_INSENSITIVE = True

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'contact@yourdomain.com')

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Using Django's default User model with UserProfile extension

# Login/Logout URLs
LOGIN_URL = '/admin/login/'

# CKEditor Configuration
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Undo', 'Redo', '-', 'Find'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor', '-', 'ShowBlocks'],
            ['Maximize', 'Source'],
            ['CodeSnippet', 'Iframe'],
            ['Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Print', 'SpellChecker'],
        ],
        'height': 400,
        'width': '100%',
        'language': 'ar',
        'contentsLangDirection': 'rtl',
        'defaultLanguage': 'ar',
        'uiColor': '#f8f9fa',
        'startupMode': 'wysiwyg',
        'enterMode': 2,  # CKEDITOR.ENTER_BR
        'shiftEnterMode': 1,  # CKEDITOR.ENTER_P
        'extraPlugins': ','.join([
            'uploadimage',
            'uploadwidget',
            'filebrowser',
            'codesnippet',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'bidi',
            'justify',
            'image2',
            'iframe',
            'find',
            'selectall',
            'smiley',
            'specialchar',
            'blockquote',
            'showblocks',
            'print',
            'preview'
        ]),
        'removePlugins': '',
        'codeSnippet_theme': 'monokai_sublime',
        'codeSnippet_languages': {
            'python': 'Python',
            'javascript': 'JavaScript',
            'html': 'HTML',
            'css': 'CSS',
            'php': 'PHP',
            'java': 'Java',
            'cpp': 'C++',
            'csharp': 'C#',
            'sql': 'SQL',
            'json': 'JSON',
            'xml': 'XML',
            'bash': 'Bash',
        },
        'allowedContent': True,
        'extraAllowedContent': 'iframe[*]; span[*]{*}; div[*]{*}; p[*]{*}; h1[*]{*}; h2[*]{*}; h3[*]{*}; h4[*]{*}; h5[*]{*}; h6[*]{*}',
        'removeButtons': '',
        'filebrowserBrowseUrl': '/blog/browse/',
        'filebrowserImageBrowseUrl': '/blog/browse/',
        'filebrowserUploadUrl': '/blog/upload/',
        'filebrowserImageUploadUrl': '/blog/upload/',
        'filebrowserFlashBrowseUrl': '/blog/browse/',
        'filebrowserFlashUploadUrl': '/blog/upload/',
        'uploadUrl': '/blog/upload/',
        'image2_alignClasses': ['image-left', 'image-center', 'image-right'],
        'image2_captionedClass': 'image-captioned',
        'image2_disableResizer': False,
        'image2_prefillDimensions': False,
        'image2_maxSize': {'width': 1200, 'height': 800},
        'format_tags': 'p;h1;h2;h3;h4;h5;h6;pre;address;div',
        'pasteFromWordPromptCleanup': True,
        'pasteFromWordRemoveFontStyles': True,
        'pasteFromWordRemoveStyles': True,
        'forcePasteAsPlainText': False,
        'autoGrow_onStartup': True,
        'autoGrow_minHeight': 400,
        'autoGrow_maxHeight': 800,
        'resize_enabled': True,
        'resize_dir': 'vertical',
        'toolbarCanCollapse': True,
        'removeDialogTabs': 'image:advanced;link:advanced',
        'magicline_everywhere': True
    },
    'awesome_ckeditor': {
        'toolbar': 'Basic',
    },
}
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/'