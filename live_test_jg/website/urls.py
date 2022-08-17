from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.loginUser, name="login"),
    path('upload', views.upload, name="upload"),
    path('about', views.about, name="about"),
    path('upload/file', views.upload_file, name="upload_file"),
    path('upload/text', views.upload_text, name="upload_file"),
]
