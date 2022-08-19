from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login_user, name="login"),
    path('upload', views.upload, name="upload"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('database', views.database, name="database"),
    path('search', views.search, name="search"),
    path('upload/file', views.upload_file, name="upload_file"),
    path('upload/text', views.upload_text, name="upload_text"),
    path('upload/edits', views.upload_edits, name="upload_edits"),
    path('upload/confirm', views.upload_confirm, name="upload_confirm"),
]
