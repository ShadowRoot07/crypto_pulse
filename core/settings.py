import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SEGURIDAD ---
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Ajuste para permitir local y dominios de Vercel
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.vercel.app',
    '0.0.0.0'
] + [h for h in os.environ.get('ALLOWED_HOSTS', '').split(',') if h]

# --- APPS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracker',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Manejo de estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls' 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'core.wsgi.application'

# --- CONFIGURACIÓN DE BASE DE DATOS INTELIGENTE ---
# Extraemos la configuración de la URL
db_from_env = dj_database_url.config(
    default=os.environ.get('DATABASE_URL'),
    conn_max_age=600,
)

# CRÍTICO: Solo activar SSL si NO es SQLite. 
# Esto evita el error 'sslmode' en GitHub Actions.
if db_from_env and db_from_env.get('ENGINE') != 'django.db.backends.sqlite3':
    db_from_env['OPTIONS'] = {'sslmode': 'require'}

DATABASES = {
    'default': db_from_env
}

# --- ARCHIVOS ESTÁTICOS ---
STATIC_URL = 'static/'
# Verificamos si la carpeta existe para evitar advertencias de Django
STATIC_DIR = os.path.join(BASE_DIR, 'static')
if os.path.exists(STATIC_DIR):
    STATICFILES_DIRS = [STATIC_DIR]
else:
    STATICFILES_DIRS = []

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuración de WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- INTERFAZ Y AUTH ---
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
