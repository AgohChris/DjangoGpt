from django.urls import path
from gptclone import views


urlpatterns = [
    path("home", views.home, name="home"),
    path("login", views.loginV, name="login"),
    path("register", views.registerV, name="register"),
    path("logout", views.deconnexion, name="logout"),
]
