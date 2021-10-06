"""
ASGI config for directory_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocalTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'directory_app.settings')

django.setup()

from channels.auth import AuthMiddleware
application = ProtocalTypeRouter({
    "http": get_asgi_application(),
})
