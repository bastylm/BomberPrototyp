"""
Django settings for bomberosM project.
"""

from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

# Load a local .env file without an extra dependency.
env_path = BASE_DIR / '.env'
if env_path.exists():
    for line in env_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip())

from django.core.exceptions import ImproperlyConfigured


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in ('1', 'true', 'yes', 'on')


SECRET_KEY = os.environ.get('SECRET_KEY', 'local-development-key-only')
DEBUG = env_bool('DEBUG', False)
if not DEBUG and SECRET_KEY == 'local-development-key-only':
    raise ImproperlyConfigured('Set a unique SECRET_KEY in the environment.')

ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h.strip()]
CSRF_TRUSTED_ORIGINS = [v.strip() for v in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if v.strip()]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'usuarios.apps.UsuariosConfig',
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

ROOT_URLCONF = 'bomberosM.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'bomberosM.wsgi.application'


# SQLite is for local development. Use a dedicated MySQL database on the VPS.
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'test_db.sqlite3',
        }
    }
else:
    db_engine = os.environ.get('DB_ENGINE', 'sqlite').strip().lower()
    if db_engine == 'sqlite':
        DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / os.environ.get('DB_NAME', 'db.sqlite3')}}
    elif db_engine == 'mysql':
        mysql_credentials = [os.environ.get(key, '').strip() for key in ('DB_NAME', 'DB_USER', 'DB_PASSWORD')]
        if not all(mysql_credentials) or any(value.startswith('set-a-unique-') for value in mysql_credentials):
            raise ImproperlyConfigured('Set dedicated demo database credentials in the environment.')
        DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql', 'NAME': os.environ.get('DB_NAME', ''), 'USER': os.environ.get('DB_USER', ''), 'PASSWORD': os.environ.get('DB_PASSWORD', ''), 'HOST': os.environ.get('DB_HOST', '127.0.0.1'), 'PORT': os.environ.get('DB_PORT', '3306'), 'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'", 'charset': 'utf8mb4'}}}
    else:
        raise ImproperlyConfigured('DB_ENGINE must be sqlite or mysql.')


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'usuarios.Usuario'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'


# Internationalization
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR] 
STATIC_ROOT = Path(os.environ.get('STATIC_ROOT', BASE_DIR / 'staticfiles'))

MEDIA_URL = '/media/'
MEDIA_ROOT = Path(os.environ.get('MEDIA_ROOT', BASE_DIR / 'media'))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de correo SMTP para notificaciones.
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_SSL = env_bool('EMAIL_USE_SSL', False)
EMAIL_USE_TLS = env_bool('EMAIL_USE_TLS', True)
# Keep the Gmail app password outside the repository in the .env/environment.
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'contactobomberosmulchen@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'Sistema Bomberos <contactobomberosmulchen@gmail.com>')

# --- CABECERAS Y MEDIDAS DE SEGURIDAD OWASP ---
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
SECURE_REFERRER_POLICY = 'same-origin'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Keep the demo's browser cookies separate from the main site on the parent domain.
SESSION_COOKIE_NAME = 'bomberprototyp_demo_sessionid'
CSRF_COOKIE_NAME = 'bomberprototyp_demo_csrftoken'
SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_DOMAIN = None
SESSION_COOKIE_SECURE = env_bool('SESSION_COOKIE_SECURE', not DEBUG)
CSRF_COOKIE_SECURE = env_bool('CSRF_COOKIE_SECURE', not DEBUG)

# --- CONFIGURACIÓN DE REGISTROS DE SEGURIDAD (LOGGING) ---
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'usuarios': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
