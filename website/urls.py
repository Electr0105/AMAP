from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search', views.search, name="search"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('searchResult', views.searchResult, name="searchResult"),
    path('upload', views.upload, name="upload"),
    path('result', views.result, name="result"),
    path('result/<int:id>', views.result),
    path('login', views.login, name="login"),
]
