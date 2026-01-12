from django.urls import path
from . import views
from .views import user_login

urlpatterns = [
     path("login/", user_login),
    path("forgot-password/", views.forgot_password),
    path("reset-password/", views.reset_password),
]