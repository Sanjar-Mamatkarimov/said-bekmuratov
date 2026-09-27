import os
import urllib.parse
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# Загружаем переменные окружения из .env / .env.local
load_dotenv()
load_dotenv('.env.local')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Папка с начальными данными (fixtures)
FIXTURE_DIRS = [BASE_DIR / 'fixtures']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-aa(z7@&!6#=*zy6ps2rtl4i79#zb1bb9jd(xu7_pq939vvr+@7',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'


def _split_csv(value):
    return [x.strip() for x in value.split(',') if x.strip()]


# Список хостов через запятую (DJANGO_ALLOWED_HOSTS)
ALLOWED_HOSTS = _split_csv(
    os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost,.vercel.app')
)


def _origin_for_host(host):
    if host.startswith('.'):
        return f'https://*{host}'
    if host in ('127.0.0.1', 'localhost'):
        return f'http://{host}'
    return f'https://{host}'


CSRF_TRUSTED_ORIGINS = [_origin_for_host(h) for h in ALLOWED_HOSTS]

# --- Telegram уведомления ---
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_ADMIN_IDS = [
    int(x.strip())
    for x in os.environ.get('TELEGRAM_ADMIN_IDS', '1258249360,8436370827').split(',')
    if x.strip().isdigit()
]

# Application definition
INSTALLED_APPS = [
    'jazzmin', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    
    # Библиотеки редактора
    'ckeditor',
    'ckeditor_uploader',
    
    'storages',
    
    # Ваше приложение
    'main',
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

ROOT_URLCONF = 'music.urls'

# --- Настройки Jazzmin ---
JAZZMIN_SETTINGS = {
    "site_title": "Школа им. С. Бекмуратова",
    "site_header": "Бекмуратов",
    "site_brand": "Админка Школы",
    "welcome_sign": "Панель управления музыкальной школой",
    "copyright": "Музыкальная школа им. С. Бекмуратова",
    "search_model": ["auth.User", "main.Event"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "main.Afisha": "fas fa-calendar-alt",
        "main.Zayavki": "fas fa-envelope-open-text",
        "main.Nagrady": "fas fa-trophy",
        "main.NashiUchitelya": "fas fa-chalkboard-teacher",
        "main.OsnovnyeNastroiki": "fas fa-cogs",
        "main.Otdeleniya": "fas fa-music",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "navbar_fixed": True,
    "sidebar_fixed": True,
}

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

WSGI_APPLICATION = 'music.wsgi.application'

# Database Connection (Neon PostgreSQL / SQLite)
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # Локальная разработка (SQLite, если DATABASE_URL не передан)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_TZ = True

# --- Статические и медиа файлы ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'static' / 'media'

# --- Настройки CKEditor ---
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono-lisa',
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        'extraPlugins': ','.join([
            'uploadimage',
            'codesnippet',
            'widget',
            'dialog',
        ]),
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Безопасность в продакшене ---
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = os.getenv("SUPABASE_S3_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("SUPABASE_S3_SECRET_KEY")
AWS_STORAGE_BUCKET_NAME = "media"
AWS_S3_ENDPOINT_URL = os.getenv("SUPABASE_S3_ENDPOINT_URL")
AWS_S3_REGION_NAME = "us-east-1"

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": os.getenv("SUPABASE_S3_ACCESS_KEY"),
            "secret_key": os.getenv("SUPABASE_S3_SECRET_KEY"),
            "bucket_name": "media",
            "endpoint_url": os.getenv("SUPABASE_S3_ENDPOINT_URL"),
            "region_name": "us-east-1",
            "file_overwrite": False,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}