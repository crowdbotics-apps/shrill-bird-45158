# asgi.py
import os
from django.core.asgi import get_asgi_application
from auction.routing import application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shrill_bird_45158.settings')

django_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_application,
    "websocket": application,
})
