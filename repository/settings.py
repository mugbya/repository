"""
Django settings for repository project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2tnv$y&q-y-o-#amd5uqh@2+@7@+quuw--a1_emdim7#@v#i=5'

# SECURITY WARNING: don't run with debug turned on in production!


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'qs',
    # 'blog',
    'user',
    'oauth',
    'haystack',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'repository.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'qs/templates'), os.path.join(BASE_DIR, 'user/templates'), ],
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

WSGI_APPLICATION = 'repository.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# full text search
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'qs.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'



LOGIN_REDIRECT_URL = '/'

# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = []

# DEBUG = False
DEBUG = True


#分页配置#######################################
PAGE_NUM = 10

#email配置#########################################
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.163.com'                       #SMTP地址 例如: smtp.163.com
# EMAIL_PORT = 25                       #SMTP端口 例如: 25
# EMAIL_HOST_USER = ''                  #我自己的邮箱 例如: xxxxxx@163.com
# EMAIL_HOST_PASSWORD = ''              #我的邮箱密码 例如  xxxxxxxxx
# EMAIL_SUBJECT_PREFIX = u'django'      #为邮件Subject-line前缀,默认是'[django]'
# EMAIL_USE_TLS = True                  #与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


try:
    from .local_settings import *
except ImportError:
    pass










