from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat.consumers import EchoConsumer, ChatConsumer
from channels.auth import AuthMiddlewareStack
from chat.token_authentication_stack import TokenAuthMiddleware

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/chat/<str:username>/', ChatConsumer),
                path('ws/chat/', EchoConsumer)
            ])
        )
    )
})