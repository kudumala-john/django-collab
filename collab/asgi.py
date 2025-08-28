import os
import sys

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collab.settings')

django_asgi_app = get_asgi_application()

import messagesapp.routing  # <--- import AFTER Django is set up

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            messagesapp.routing.websocket_urlpatterns
        )
    ),
})
