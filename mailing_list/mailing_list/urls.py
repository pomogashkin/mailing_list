from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from main.views import ClientViewSet, MessageViewSet, MailingListViewSet
from .yasg import swaggerurlpatterns


router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'mailing-lists', MailingListViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include("rest_framework.urls", namespace="rest_framework"))
]

urlpatterns += swaggerurlpatterns
