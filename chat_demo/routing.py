from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat.consumers import EchoConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/chat/', EchoConsumer)
    ])
})