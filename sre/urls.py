from django.urls import path
from .views import *

urlpatterns = [
    path('status_cake/webhook/', status_cake_webhook),
    path('git/webhook/', git_webhook),
]
