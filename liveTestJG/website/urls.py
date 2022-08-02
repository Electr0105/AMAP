from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.loginUser, name="login"),
    path('upload', views.upload, name="upload"),
    path('about', views.about, name="about"),
]
