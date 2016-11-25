DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'new_repository',
        'USER': 'mugbya',
        'PASSWORD': 'a13990769335w',
        'HOST': 'localhost',
        'PORT': '5432',

    }
}

# 邮件服务器配置

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'  # SMTP地址 例如: smtp.163.com
EMAIL_PORT = 25  # SMTP端口 例如: 25
EMAIL_HOST_USER = '741507554@qq.com'  # 我自己的邮箱 例如: xxxxxx@163.com
EMAIL_HOST_PASSWORD = 'm9527133t'  # 我的邮箱密码 例如  xxxxxxxxx
EMAIL_SUBJECT_PREFIX = u'django'  # 为邮件Subject-line前缀,默认是'[django]'
EMAIL_USE_TLS = True  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

GITHUB_CLIENT_ID = 'dd90d6225d6bb60bf7a5'
GITHUB_CLIENT_SECRET = '1e8ae44e78831f1831e7be2755201d30b3ea2e0c'
GITHUB_CALLBACK = 'http://127.0.0.1:8000/oauth/github/verify/'
