from django.urls import path
from .views import support_form

urlpatterns = [
    path('submit/', support_form, name='support_form'),
    path('test/', support_form, name='test'),
]
