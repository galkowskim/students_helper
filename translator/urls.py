from django.urls import path
from .views import translate_app

urlpatterns = [
    path('', translate_app, name='translate'),
]