from django.urls import path, include
from chat.views import ThreadView

urlpatterns = [
    path('<str:username>/', ThreadView.as_view())
]