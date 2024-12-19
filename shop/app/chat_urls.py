from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *
from django.contrib.auth.views import *
from .api import MessageModelViewSet, UserModelViewSet

router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UserModelViewSet, basename='user-api')
urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    path('', login_required(
        TemplateView.as_view(template_name='chat/chat.html')), name='help_chat'),
]
print(urlpatterns)