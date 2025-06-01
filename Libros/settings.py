# Libros/settings.py
import os
from pathlib import Path
import django

BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad: obtener SECRET_KEY de variable de entorno para no exponerla en el código
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-key-for-development')

# DEBUG debe ser False en producción; Render define la variable RENDER para detectar entorno
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

# ALLOWED_HOSTS debe incluir el hostname que Render asigna a tu app
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')
if not ALLOWED_HOSTS:
    # Si no está configurado, para desarrollo permite localhost
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Aplicaciones.repaso',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para servir estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Libros.urls'

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
            ],
        },
    },
]

# Configuración base de datos MySQL con variables de entorno
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'Libros'),
        'USER': os.getenv('MYSQL_USER', 'root'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', ''),
        # IMPORTANTE: Cambia 'localhost' por el host remoto de tu base de datos MySQL en Render o externa
        'HOST': os.getenv('MYSQL_HOST', 'localhost'),
        'PORT': os.getenv('MYSQL_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# Parche para evitar error con RETURNING en MariaDB < 10.5 o MySQL sin soporte
if django.VERSION >= (4, 2):
    from django.db.backends.mysql.features import DatabaseFeatures
    DatabaseFeatures.can_return_columns_from_insert = False

# Internacionalización
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Carpeta donde collectstatic guarda los archivos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'Libros', 'static'),  # Carpeta con tus archivos estáticos locales
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # WhiteNoise para producción

# Campo por defecto para modelos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración login
LOGIN_URL = 'login'              # URL a la que se redirige si no está autenticado
LOGIN_REDIRECT_URL = 'inicio'   # URL tras login exitoso
LOGOUT_REDIRECT_URL = 'login'   # URL tras logout
