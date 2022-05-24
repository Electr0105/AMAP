from django.shortcuts import render
from .models import Vase
import os

# Create your views here.
def home(request):
    objects = Vase.objects.all
    return render(request, 'home.html', {'all':objects})

def search(request):
    objects = Vase.objects.all
    return render(request, 'search.html', {'all':objects})

def about(request):
    return render(request, 'about.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def searchResult(request):
    if request.method == "POST":
        vaseRef = request.POST.get("vaseRef","")
        collectionName = request.POST.get("collectionName","")
        objects = Vase.objects.filter(collectionName__icontains=vaseRef or collectionName__icontains=collectionName)
        return render(request, 'searchResult.html', {"all":objects,"vaseRef":vaseRef})
    else:
        return render(request, 'search.html')
