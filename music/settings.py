import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv


# ============================================================
# ENV
# ============================================================

load_dotenv()
load_dotenv(".env.local")


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# FIXTURES
# ============================================================

FIXTURE_DIRS = [
    BASE_DIR / "fixtures",
]


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-aa(z7@&!6#=*zy6ps2rtl4i79#zb1bb9jd(xu7_pq939vvr+@7",
)

DEBUG = os.environ.get(
    "DJANGO_DEBUG",
    "False",
).lower() == "true"


def _split_csv(value):
    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


ALLOWED_HOSTS = _split_csv(
    os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost,.vercel.app",
    )
)


def _origin_for_host(host):
    if host.startswith("."):
        return f"https://*{host}"

    if host in ("127.0.0.1", "localhost"):
        return f"http://{host}"

    return f"https://{host}"


CSRF_TRUSTED_ORIGINS = [
    _origin_for_host(host)
    for host in ALLOWED_HOSTS
]


# ============================================================
# TELEGRAM
# ============================================================

TELEGRAM_BOT_TOKEN = os.environ.get(
    "TELEGRAM_BOT_TOKEN",
    "",
)

TELEGRAM_ADMIN_IDS = [
    int(item.strip())
    for item in os.environ.get(
        "TELEGRAM_ADMIN_IDS",
        "1258249360,8436370827",
    ).split(",")
    if item.strip().isdigit()
]


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # Admin theme
    "jazzmin",

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",

    # CKEditor
    "ckeditor",
    "ckeditor_uploader",

    # S3 storage
    "storages",

    # Main application
    "main",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "music.urls"

WSGI_APPLICATION = "music.wsgi.application"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ============================================================
# JAZZMIN
# ============================================================

JAZZMIN_SETTINGS = {
    "site_title": "Школа им. С. Бекмуратова",

    "site_header": "Бекмуратов",

    "site_brand": "Админка Школы",

    "welcome_sign": "Панель управления музыкальной школой",

    "copyright": "Музыкальная школа им. С. Бекмуратова",

    "search_model": [
        "auth.User",
        "main.Event",
    ],

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


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.environ.get("DATABASE_URL")


if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Asia/Bishkek"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

# CSS / JS / favicon / статические изображения
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================================================
# SUPABASE S3 STORAGE
# ============================================================

SUPABASE_S3_ACCESS_KEY = os.environ.get(
    "SUPABASE_S3_ACCESS_KEY",
    "",
)

SUPABASE_S3_SECRET_KEY = os.environ.get(
    "SUPABASE_S3_SECRET_KEY",
    "",
)

SUPABASE_S3_ENDPOINT_URL = os.environ.get(
    "SUPABASE_S3_ENDPOINT_URL",
    "",
)

SUPABASE_S3_REGION = os.environ.get(
    "SUPABASE_S3_REGION",
    "us-east-1",
)


# Django-storages / boto3
AWS_ACCESS_KEY_ID = SUPABASE_S3_ACCESS_KEY

AWS_SECRET_ACCESS_KEY = SUPABASE_S3_SECRET_KEY

AWS_STORAGE_BUCKET_NAME = "media"

AWS_S3_ENDPOINT_URL = SUPABASE_S3_ENDPOINT_URL

AWS_S3_REGION_NAME = SUPABASE_S3_REGION

# Supabase рекомендует path-style для S3 endpoint
AWS_S3_ADDRESSING_STYLE = "path"

# Supabase S3 использует Signature V4
AWS_S3_SIGNATURE_VERSION = "s3v4"

# Не перезаписывать одинаковые имена файлов
AWS_S3_FILE_OVERWRITE = False

# Публичные URL без подписанных query-параметров.
# Это предполагает, что bucket "media" публичный.
AWS_QUERYSTRING_AUTH = False

# HTTPS
AWS_S3_USE_SSL = True


# ============================================================
# DJANGO STORAGE BACKENDS
# ============================================================

STORAGES = {
    # ВСЕ FileField / ImageField / CKEditor uploads
    # будут сохраняться в Supabase Storage.
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },

    # CSS / JS / static files
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# ============================================================
# CKEDITOR
# ============================================================

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    "default": {
        "skin": "moono-lisa",

        "toolbar": "full",

        "height": 300,

        "width": "100%",

        "extraPlugins": ",".join(
            [
                "uploadimage",
                "codesnippet",
                "widget",
                "dialog",
            ]
        ),
    },
}


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# PROXY / HTTPS
# ============================================================

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


# ============================================================
# PRODUCTION SECURITY
# ============================================================

if not DEBUG:

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_SSL_REDIRECT = True

    SECURE_HSTS_SECONDS = 31536000

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_REFERRER_POLICY = (
        "strict-origin-when-cross-origin"
    )