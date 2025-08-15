from pathlib import Path
from django.conf import settings
from django.conf.urls.static import static
import os
import environ
import dj_database_url

env = environ.Env()


BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
# print("SECRET_KEY:", env('SECRET_KEY'))

#SECRET_KEY = env('SECRET_KEY')
SECRET_KEY = "django-insecure-o(w)kc$sq8$u&lhl!se*#lyflm2%&@s30z^)yl7h(^korh7lmu"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = [
    'koudem.com',
    'www.koudem.com',
    'tu-proyecto.railway.app',  # Dominio de Railway
    'localhost',
    '127.0.0.1'
]


RECAPTCHA_PUBLIC_KEY = '6LepmP4pAAAAAO1NLx2VU1GTCQPT_gJwpWNWO8KS'
RECAPTCHA_PRIVATE_KEY = '6LepmP4pAAAAAGcvVDT5YBYsnc9US6MoWucNj6Az'


CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",  # Añade aquí los orígenes permitidos
    "https://tuotrodominio.com",
    # Añade más orígenes si es necesario
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,"media")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'index',
    'course',
    'menu',
    'core',
    'payments',
    'django_recaptcha'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    

]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'koudem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'koudem.wsgi.application'


if os.getenv('RAILWAY_ENVIRONMENT') == 'production':
    database_url = os.getenv('DATABASE_URL') or os.getenv('DATABASE_PUBLIC_URL')
    DATABASES = {
        'default': dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'koudem_local',
            'USER': 'postgres',
            'PASSWORD': 'gordo1968',
            'HOST': 'localhost',
            'PORT': '5432',
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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'user.CustomUser'


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Para producción
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Para desarrollo







DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGOUT_REDIRECT_URL = 'dashboard'

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[
    'https://koudem.com',
    'https://www.koudem.com',
    'https://*.railway.app'
])

CSRF_COOKIE_SECURE=False


# CSRF_COOKIE_DOMAIN = 'localhost'

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')

#CSRF_COOKIE_SECURE = True  # Si estás usando HTTPS
CSRF_COOKIE_HTTPONLY = True



RECAPTCHA_USE_SSL = True  # opcional

RECAPTCHA_PUBLIC_KEY = '6LepmP4pAAAAAO1NLx2VU1GTCQPT_gJwpWNWO8KS'
RECAPTCHA_PRIVATE_KEY = '6LepmP4pAAAAAGcvVDT5YBYsnc9US6MoWucNj6Az'

#SILENCED_SYSTEM_CHECKS=['django_recaptcha.recaptcha_test_key_error']

RECAPTCHA_DOMAIN = 'www.recaptcha.net'

#RECAPTCHA_PROXY = {'http' : 'http://127.0.0.1:8000'}


#Email Setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'martinc1399@gmail.com'  # Cambia esto
EMAIL_HOST_PASSWORD = 'thfoiibcdenkmvpv'   # Usa una contraseña de app

PASSWORD_RESET_TIMEOUT = 14400

LOGIN_URL= '/user/login/'

# Establecer el huso horario global
TIME_ZONE = 'America/Mexico_City'  # Ejemplo para Ciudad de México

# Activar soporte para husos horarios
USE_TZ = True  # True habilita el soporte de husos horarios


# Tiempo de vida de la sesión en segundos (ej. 30 minutos = 1800 segundos)
SESSION_COOKIE_AGE = 10800  

# Renovar la sesión con cada request (opcional)
SESSION_SAVE_EVERY_REQUEST = True


print("RAILWAY_ENVIRONMENT:", os.getenv("RAILWAY_ENVIRONMENT"))
print("DATABASE_URL:", os.getenv("DATABASE_URL"))
print("DATABASE_PUBLIC_URL:", os.getenv("DATABASE_PUBLIC_URL"))
