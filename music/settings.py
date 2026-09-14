import os
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env / .env.local (для локальной разработки)
load_dotenv()
load_dotenv('.env.local')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Папка с начальными данными (fixtures)
FIXTURE_DIRS = [BASE_DIR / 'fixtures']

# SECURITY WARNING: keep the secret key used in production secret!
# Задайте DJANGO_SECRET_KEY в переменных окружения Vercel.
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
    # Django 5+ поддерживает wildcard в CSRF_TRUSTED_ORIGINS (https://*.vercel.app)
    if host.startswith('.'):
        return f'https://*{host}'
    if host in ('127.0.0.1', 'localhost'):
        return f'http://{host}'
    return f'https://{host}'


# Доверенные origins всегда вычисляются из ALLOWED_HOSTS, чтобы никак не
# зависеть от домена и не сломаться от неверного env (Django 5+ поддерживает
# wildcard https://*.vercel.app). Для своего домена — добавьте его в DJANGO_ALLOWED_HOSTS.
CSRF_TRUSTED_ORIGINS = [_origin_for_host(h) for h in ALLOWED_HOSTS]

# --- Telegram уведомления ---
# Задайте TELEGRAM_BOT_TOKEN и TELEGRAM_ADMIN_IDS в переменных окружения Vercel.
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
    "search_model": ["auth.User", "main.Afisha"],
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

# Database
# В продакшене (Vercel) задайте DATABASE_URL, например postgres://user:pass@host:5432/dbname
if os.environ.get('DATABASE_URL'):
    _db_url = urllib.parse.urlparse(os.environ['DATABASE_URL'])
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': _db_url.path.lstrip('/'),
            'USER': _db_url.username,
            'PASSWORD': _db_url.password,
            'HOST': _db_url.hostname,
            'PORT': _db_url.port,
        }
    }
else:
    # Локальная разработка
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
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles' # Важно для collectstatic

# Медиафайлы живут внутри static/ — Vercel собирает их через collectstatic и отдаёт с CDN
MEDIA_URL = '/static/media/'
MEDIA_ROOT = BASE_DIR / 'static' / 'media'

# --- Настройки CKEditor (Исправлено под версию django-ckeditor) ---
CKEDITOR_UPLOAD_PATH = "uploads/" # Папка для загрузки в media/
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono-lisa',
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        'extraPlugins': ','.join([
            'uploadimage', # Плагин для загрузки перетаскиванием
            'codesnippet',
            'widget',
            'dialog',
        ]),
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Безопасность в продакшене (Vercel завершает TLS) ---
# SECURE_PROXY_SSL_HEADER нужен всегда (Vercel шлёт X-Forwarded-Proto),
# чтобы request.is_secure() был True и CSRF-проверка Origin совпадала.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
