import os
from django.contrib.messages import constants as messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = os.getenv("STATIC_URL", "/static/")
STATIC_ROOT = os.getenv("STATIC_ROOT", os.path.join(BASE_DIR, 'design', 'static_root'))
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "design", "static"),
)

SECRET_KEY = '6sgy3tg4j4vm%&_(@2s_3699u3v^7=_-txpp+j8keks#xtkt!x'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',       # Нэмэлт, хэрэглэгч статик файлууд дагаад устана

    'modules.base',
    'modules.ctf',
    'modules.electronics',
    'modules.mathematics',
    'modules.network',

    'martor',                           # Нэмэлт, CTF -ийн бодлого нэмэх хэсэг дээр markdown утга авна
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Coming `django-session-timeout` used for auto logout users
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
]

ROOT_URLCONF = 'oyucore.urls'
TEMPLATE_DIR = os.path.join(BASE_DIR, "design", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "design", "static")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'oyucore.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
 }

AUTH_USER_MODEL = "base.OyuUser"

LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/'

LANGUAGE_CODE = 'mn'

TIME_ZONE = 'Asia/Ulaanbaatar'

USE_I18N = True

USE_L10N = True

USE_TZ = False

PROJECT_ROOT = os.path.join(os.path.abspath(__file__))

STATIC_URL = '/static/'
STATICFILES_DIR = [STATIC_DIR]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Sessions
SESSION_EXPIRE_SECONDS = 3600  # 1 hour
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Martur Configs
MARTOR_ENABLE_CONFIGS = {
    'emoji': 'false',
    'imgur': 'false',
    'mention': 'false',
    'jquery': 'true',
    'living': 'false',
    'spellcheck': 'false',
    'hljs': 'false',
}

MARTOR_TOOLBAR_BUTTONS = [
    'bold', 'italic', 'pre-code', 'unordered-list', 'link',
]
MARTOR_ENABLE_LABEL = False
MARTOR_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.smarty',
    'markdown.extensions.fenced_code',
]

# HashID
HASHID_FIELD_SALT = "a long and secure salt value that is not the same as SECRET_KEY"