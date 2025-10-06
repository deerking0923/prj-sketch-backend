from pathlib import Path
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# 환경변수에서 읽어오기
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-_q5&dd*_af5+@spi@)q2!68tme1p3)4%67%xm#4=^hzvtu$yju')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
SERVER_IP = os.getenv('SERVER_IP', 'localhost')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    SERVER_IP,
    'realdeerworld.com',
    'www.realdeerworld.com'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'converter.apps.ConverterConfig',
    'corsheaders', 
]

MIDDLEWARE = [
    # CORS 미들웨어는 최상단에 있어야 합니다!
    'corsheaders.middleware.CorsMiddleware', 
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- CORS Configuration ---
CORS_ALLOWED_ORIGINS = [
    # 로컬 개발 환경
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    
    # 서버 환경 - Next.js 프론트엔드
    f"http://{SERVER_IP}:3000",
    
    'http://realdeerworld.com',
    'http://www.realdeerworld.com',

    # Spring Boot 백엔드
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    f"http://{SERVER_IP}:8080",


]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_CREDENTIALS = True