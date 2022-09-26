from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login_user, name="login"),
    path('upload', views.upload, name="upload"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('database', views.database, name="database"),
    path('advanced_search', views.advanced_search, name="advanced_search"),
    path('search_result', views.search_result, name="search_result"),
    path('upload/confirm', views.upload_confirm, name="upload_confirm"),
    path('vase/<int:id>', views.vase_page, name="vase_page"),
    path('upload/file', views.upload_file, name="upload_file"),
    path('upload/text', views.upload_text, name="upload_text")
]
