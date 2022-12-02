'''
ASGI config for drf_pro project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
'''

import os
import pathlib

from django.core.asgi import get_asgi_application

from dotenv import load_dotenv

env_path = pathlib.Path('.').parent / '.env'
load_dotenv(dotenv_path=env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_pro.settings')

application = get_asgi_application()
