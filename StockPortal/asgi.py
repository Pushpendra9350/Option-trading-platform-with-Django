"""
ASGI config for StockPortal project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from OptionApp.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StockPortal.settings')

# Since we'll be using WebSockets instead of HTTP to communicate from the client 
# to the server, we need to wrap our ASGI config with ProtocolTypeRouter in asgi.py
# This router will route traffic to different parts of the web application depending on the protocol used.
# Basically it routes the requests to accordingly to https or websocket
application = ProtocolTypeRouter({
    # Used to get asgi supprt for django 
    'http': get_asgi_application(),
    # Routes http or websocket type connections via their HTTP path(for URLRouter)
    'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns))
})