import os
from decouple import config
from dj_database_url import parse as db_url

# 在项目中构建如下路径:BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 安全警告:请对生产中使用的密钥保密!
SECRET_KEY = config('SECRET_KEY')


# 安全警告:不要在生产环境中运行调试状态!
DEBUG = config('DEBUG', default=False, cast=bool)


# 应用程序定义
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方包
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'corsheaders',
    # 项目App
    "apps.authentication",
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 跨域中间件
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定义中间件添加在最后
    'core.LogMiddleware.RequestLogMiddleware'
]

# 自定义用户模型
AUTH_USER_MODEL = 'authentication.User'
# 自定义用户验证
AUTHENTICATION_BACKENDS = (
    'core.Authenticate.CustomBackend',
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = 'drf_pro.urls'


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


WSGI_APPLICATION = 'drf_pro.wsgi.application'

# CORS 白名单
CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "https://juejin.cn"
)
# CORS 正则表达式白名单
CORS_ORIGIN_REGEX_WHITELIST = ()

# 允许所有地址跨域访问
# CORS_ORIGIN_ALLOW_ALL = True


# Database
# 如果您希望使用默认的sqlite以外的其他数据库
# 确保在你的env文件中更新DATABASE_URL的值
DATABASES = {
    'default': config(
        'DATABASE_URL',
        cast=db_url
    )
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


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # 激活drf_spectacular
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # 全局异常捕获
    'EXCEPTION_HANDLER': 'core.ExceptionHandler.common_exception_handler'
}


# drf_spectacular配置
SPECTACULAR_SETTINGS = {
    'TITLE': 'drf_pro  Project API',
    'VERSION': '1.0.0',
}

ALLOWED_HOSTS = ['*']


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

LOGGING = {
    # 版本
    'version': 1,
    # 是否禁止默认配置的记录器
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(path)s %(method)s %(username)s %(code)s '
                      f'%(sip)s\n%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    # 过滤器
    'filters': {
        'request_info': {'()': 'core.LogMiddleware.RequestLogFilter'},
    },
    'handlers': {
        # 标准输出
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'api_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs/api.log"),
            'formatter': 'standard',
            'filters': ['request_info'],
            'when': 'MIDNIGHT',
            'backupCount': 7,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            "propagate": False
        },
        # 'django.db.backends': {
        #     'handlers': ['api_handler'],
        #     'level': 'DEBUG',
        #     'propagate': False
        # },
        'api': {
            'handlers': ['api_handler'],
            'level': 'INFO',
            "propagate": False
        }
    }
}
