from django.shortcuts import render
from .models import Vase
import mysql.connector
import os


# Create your views here.
def home(request):
    objects = Vase.objects.all
    return render(request, 'home.html', {'all':objects})

def search(request):
    return render(request, 'search.html', {})
