from django.urls import path, include
from rest_framework.routers import DefaultRouter

from support.views import SupportRequestViewSet


router = DefaultRouter()
router.register(
    r'support-requests',
    SupportRequestViewSet,
    basename="supportrequest"
)

urlpatterns = [
    path('', include(router.urls)),
]
