# drf_pro

👏欢迎来到我的DRF进阶之路💐💐

**Start From Today** ⛽️⛽️⛽️⛽️⛽️⛽️   2022.3.21 Monday

- [drf\_pro](#drf_pro)
    - [什么是DRF](#什么是drf)
    - [项目初始化](#项目初始化)
    - [第一个APP：User](#第一个appuser)
      - [注册接口的实现](#注册接口的实现)
      - [登录接口的实现](#登录接口的实现)
    - [Permissions权限验证](#permissions权限验证)
      - [DRF提供的权限验证类型](#drf提供的权限验证类型)
      - [在接口类中的使用](#在接口类中的使用)
      - [在方法中使用](#在方法中使用)
      - [自定义权限认证类](#自定义权限认证类)
      - [自定义接口类中权限验证](#自定义接口类中权限验证)
    - [DRF写出优美的logs](#drf写出优美的logs)
      - [自定义日志记录配置](#自定义日志记录配置)

### 什么是DRF

这里引用一下官方文档的说明：

Django REST framework 框架是一个用于构建Web api的强大而灵活的工具包。  

优势:  
- Web可浏览API对开发人员来说是一个巨大的可用性优势。 
- 认证策略包括OAuth1a和OAuth2包。 
- 支持ORM和非ORM数据源的序列化。 
- 完全可定制——如果不需要更强大的特性，
- 只需使用常规的基于函数的视图。 广泛的文档和强大的社区支持。 
- 被国际公认的公司使用和信任，包括Mozilla, Red Hat, Heroku，和Eve

总而言之，我的感觉是相比较于Django来说Django REST framework的确是强大又灵活，直观的感受是在接口代码的编写中，强大的序列化器让你飘飘欲仙 👋

回归正传 🤌 look down 🧐

main分支 🌹

### 项目初始化

**!!!!注意第一步不要迁移数据库！！！**

🈲️ python manage.py makemigrations & python manage.py migrate

首先你需在你的 settings.py: INSTALLED_APPS 中加入以下两个drf必须的app

- rest_framework 是为了把drf框架引入到你的项目

- rest_framework.authtoken 会在你第一次迁移数据库的时候生成用户Token表


```python

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken'
]

```

接下来把下面的 REST_FRAMEWORK 拷贝到你的setting.py文件中，里边包含了一些drf的基本配置

```python

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DEFAULT_RENDER_CLASSES': [
        'rest_framework.renders.JSONRenderer',
        'rest_framework.renders.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ]
  }
```

数据库的设置Django默认数据库为sqlite 你可以把他换成你的mysql数据库，只需要简单的配置 settings.py: DATABASES 即可

```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DRF_TEST1',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}
```
配置完DATABASE之后，你需要在你的项目初始文件夹的__init__.py中添加以下内容，以确保连接数据库

DRF_Professional/__init__.py

```python
import pymysql
pymysql.install_as_MySQLdb()
```

至此基本配置完成✅✅✅✅✅


### 第一个APP：User

Django框架在你第一次进行数据库迁移的时候会默认给你生成User表

当然你也可以继承默认User表来创建自己的User表

首先你需要先start一个 user app：python manage.py startapp user

之后将此app注册到你的setting.py: INSTALLED_APPS中

在user/models.py中写入以下代码来创建你的user表：

可添加额外你所需要字段

```python

SEX_CHOICES = [
    (1, '男'),
    (2, '女')
]

class User(AbstractUser):
    nickname = models.CharField(
        max_length=150
    )
    sex = models.IntegerField(
        choices=SEX_CHOICES
    )

    def __str__(self):
        return self.nickname

    class Meta:
        # 默认id升序排序
        ordering = ['-id']
        # 数据库表名
        db_table = 'user'
```

至此 可进行第一次数据库迁移 ✌️ ✌️

**可前往apps/user/views.py 中查看万能注册、登录接口**

#### 注册接口的实现

首先你需要定义好自己的注册序列化器

apps/user/serializer.py

```python

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)
    username = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'id',
            'nickname',
            'username',
            'password',
            'confirm_password',
            'sex',
            'code'
        ]

    default_error_messages = {
        'code_error': '验证码不正确',
        'password_error': '两次密码输入不正确',
        "username_error": '手机号码格式不正确',
    }

    def validate(self, attrs):
        if not re.match(r'^1[3-9]\d{9}$', attrs['username']):
            raise ParamsException(self.error_messages['username_error'], 422)
        if attrs.get('code') != '123':
            raise ParamsException(self.error_messages['code_error'], 422)
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ParamsException(self.error_messages['password_error'], 422)
        del attrs['confirm_password']
        del attrs['code']
        attrs['password'] = make_password(attrs['password'])
        return attrs
```

因为注册需要将信息写入到User表中，所以该序列化器继承自 serializers.ModelSerializer

此序列化器主要是对注册字段的校验，所以重写了validate方法

主要校验的字段为 username password confirm_password code(短信验证码)，所以将他们定义到了序列化器中并对其在validate方法中进行了校验

ParamsException异常为自定义异常 utils/exception.py, 同时自定义了drf异常捕获

**定义好之后需要加在settings.py：REST_FRAMEWORK中**

```python
REST_FRAMEWORK = {
    # 异常返回格式控制
    'EXCEPTION_HANDLER': 'utils.exception.custom_exception_handler',
}
```

apps/user/views.py

```python
class UserSignupAPIView(CreateAPIView):
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.instance

        Token.objects.get_or_create(user=user)
        data = {"code": 200, "msg": "成功"}

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )
```
注册api继承了generics的CreateAPIView，在这里你可以重写post方法来定制你自己的api， 注册成功将Token记录到表中

Token表：from rest_framework.authtoken.models import Token


#### 登录接口的实现

apps/user/serializer.py

```python
class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': '用户已被禁用',
        'invalid_credentials': '账号或密码无效'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise ParamsException(self.error_messages['inactive_account'], 404)
            return attrs
        else:
            raise ParamsException(self.error_messages['invalid_credentials'], 404)
```

因为登录主要校验username和password的真实性，所以此序列化器继承自serializers.Serializer，重写__init__方法加入user，使其序列化成功后可携带user信息

重写validate方法完成username和password的校验

apps/user/views.py

```python
class UserSigninAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSigninSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        token, _ = Token.objects.get_or_create(user=user)
        data = {"code": 200, "msg": "成功", "data": {"token": token.key, "nickname": user.nickname}}

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
```
api接口继承自GenericAPIView基础类，并重写post方法完成登录的校验

### Permissions权限验证

**官方解释：**

> 权限检查总是在视图的最开始运行，然后才允许其他代码继续。权限检查通常使用请求中的身份验证信息。用户和请求。验证属性，以确定传入请求是否应被允许。  权
> 限用于授予或拒绝不同类型的用户对API不同部分的访问。  
> 最简单的权限样式是允许访问任何经过身份验证的用户，拒绝访问任何未经身份验证的用户。这对应于REST框架中的IsAuthenticated类。

其实意思很简单就是你把权限验证加上，如果写单个的接口（直接def或者继承单一的generics类）这样就可以验证所有用户访问，如果用户没有权限，那就会401

如果是直接继承ModelViewSet 生成标准的restful接口时，你只想让普通用户使用get接口，其他类型接口也可以对对应的权限验证 🐂🐂🐂

#### DRF提供的权限验证类型

- AllowAny：允许不受限制的访问，不管请求是否经过了身份验证。
- IsAuthenticated：拒绝任何未经身份验证的用户的权限，而允许其他用户的权限。如果您希望您的API仅对注册用户可访问，则此权限是合适的。
- IsAdminUser：拒绝任何用户的权限，除非use.is_staff为True，在这种情况下允许访问。
- IsAuthenticatedOrReadOnly：允许经过身份验证的用户执行任何请求。对于未获授权用户的请求，会被允许GET、HEAD或OPTIONS。

#### 在接口类中的使用

```python
class UserSigninAPIView(GenericAPIView):
    permission_classes = [IsAdminUser]
    ...
    ...
```

#### 在方法中使用

drf提供了permission_classes装饰器来方便你的使用
```python
@permission_classes([IsAdminUser])
def user_signin(request):
    pass
```

#### 自定义权限认证类

因为使用drf默认的验证类时，在Postman等类似平台进行接口测试容易引发CSRF认证错误❌，所以自定义验证类。

自定义验证类需要继承自permissions.BasePermission，并且重写has_permission方法来定义您自己的验证类

has_permission方法return True或者False

```python
class IsMyUser(permissions.BasePermission):
    """
    仅允许Token验证成功的用户访问
    """

    default_error_messages = {
        'invalid__token': 'token无效'
    }

    def has_permission(self, request, view):
        token = request.META.get("HTTP_TOKEN")
        user_token = Token.objects.filter(key=token).first()
        if not user_token:
            raise ParamsException(self.default_error_messages['invalid__token'], 401)
        if timezone.now() > (user_token.created + timedelta(days=TOKEN_LIFETIME)):
            raise ParamsException(self.default_error_messages['invalid__token'], 401)
        return True

```

#### 自定义接口类中权限验证

如果你在一个接口类中定义了多个接口，但是你想让不同的用户访问到不同类型的接口，您就需要重写接口类中的get_permissions方法

以下面接口为例

ModelViewSet中会有list、retrieve、create...等方法，你可以在get_permissions通过self.action来获得他们并指定这些接口可访问的用户

```python
class VideoModelViewSet(ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    def get_permissions(self):
        if self.action == "retrieve":
            return [IsExeUser()]
        return [IsAdmin()]
    ...
    ...
```

### DRF写出优美的logs

Django使用并扩展了Python的内置logging模块来执行系统日志。
一份 Python logging 可以有下面三个部分组成：

- Loggers：当 logger 处理一条消息时，会将自己的日志级别和这条消息的日志级别做对比。如果消息的日志级别匹配或者高于 logger 的日志级别，它就会被进一步处理。否则这条消息就会被忽略掉。当logger 确定了一条消息需要处理之后，会把它传给 Handler。
- Handlers：handler可以帮助logger将日志写入到文件中
- Formatters：在这里你可以规定日志写入到文件的格式

**例子**

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        }
    },
    'loggers': {
        '': {
            'handlers': ['write'],
            'level': 'INFO',
        }
    },
    'handlers': {
        'write': {
            'filename': 'logs/debug.log',
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志文件大小：5M
            'maxBytes': 5 * 1024 * 1024,
            'encoding': "utf-8",
            'formatter': 'verbose'
        }
    }
}
```
这样的话每当有请求时，Django就会自动的把log记录到你的logs/debug.log文件中✅✅
 
 
#### 自定义日志记录配置

记录优美的log是每一个程序员的追求✌️✌️✌️

如果你想要来配置自己的个性话log的，你需要通过自定义中间件来实现

直接上代码 👴

自定义日志中间件
```python
from __future__ import unicode_literals
import logging
import time

class LoggingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            res = response.data
        except Exception:
            res = None
        if request.method != 'GET':
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            logging.info("{} {} {} {} {} {}\nres:{}".format(
                localtime, request.user, request.method, request.path,
                response.status_code, response.reason_phrase, res))
        return response
```

settings.py中间件的引入

```python
MIDDLEWARE = [
     ...
     ...
    'utils.LoggingMiddleware.LoggingMiddleware'
]
```

LOGGING配置

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        '': {
            'handlers': ['write'],
            'level': 'DEBUG',
        }
    },
    'handlers': {
        'write': {
            'filename': 'logs/debug.log',
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 5 * 1024 * 1024,
            'encoding': "utf-8"
        }
    }
}
```

这样的话你就能拥有你自己优美的log啦
<img width="1126" alt="image" src="https://user-images.githubusercontent.com/102028148/159929522-d200839d-78ab-4a62-8585-64d29e65b2ea.png">


