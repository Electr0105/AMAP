from django.shortcuts import render
from .models import Vase
from django.db.models import Q
from django.db.models import CharField
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .customPython.fileUpload import *
from .customPython.databaseScripts import insertToTable
from itertools import chain
from django.http import Http404
from django.contrib.auth import authenticate, login

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def search(request):
    objects = Vase.objects.all()
    return render(request, 'search.html', {'all':objects})

def about(request):
    return render(request, 'about.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def upload(request):
    if request.POST.get("fileName"):
        if request.method == "POST":
            fileValue = request.FILES["fileName"].read()
            # insertToTable(fileValue)
            return render(request, 'upload.html', {"fileValue":fileValue})
        else:
            return render(request, 'upload.html', {})
    else:
        noFile = "Empty File"
        return render(request, 'upload.html', {"noFile":noFile})

def searchResult(request):
    if request.method == "POST":
        vaseId = request.POST.get("vaseId","")
        vaseRef = request.POST.get("vaseRef","")
        collectionName = request.POST.get("collectionName","")
        provenanceName = request.POST.get("provenanceName","")
        searchDatabase = request.POST.get("searchDatabase", "")
        valueSet = [vaseId, vaseRef, collectionName, provenanceName]
        nameSet = {"vaseId":vaseId, "vaseRef":vaseRef, "collectionName":collectionName,"provenanceName":provenanceName}
        allVases = Vase.objects.all()
        sortedVases = Vase.objects.filter(vaseRef__icontains=vaseRef,vaseId__icontains=vaseId, collectionName__icontains=collectionName, provenanceName__icontains=provenanceName)
        if(not searchDatabase):
            if not "" in valueSet:
                return render(request, 'searchResult.html', {"all":allVases})
            else:
                return render(request, 'searchResult.html', {"sortedVases":sortedVases,"vaseId":vaseId, "collectionName":collectionName, "provName":provenanceName, "nameSet":nameSet})
        else:

            vaseIdMatch = Vase.objects.filter(vaseId__iexact=searchDatabase)
            collectionNameMatch = Vase.objects.filter(collectionName__icontains=searchDatabase)
            provenanceNamemMatch = Vase.objects.filter(provenanceName__icontains=searchDatabase)
            vaseSelection = list(chain(vaseIdMatch, collectionNameMatch, provenanceNamemMatch))
            return render(request, 'searchResult.html', {"databaseSearch":vaseSelection, "searchedTerm":searchDatabase})
    else:
        return render(request, 'seach.html',{})
            # print(queries)
            # qs = Q()
            # for query in queries:
            #     qs = qs | query
            # if(not vaseId):
            #     databaseSearch = Vase.objects.filter(qs)
            # else:
            #     databaseSearch = Vase.objects.filter(vaseId, qs)
            # return render(request, 'searchResult.html', {"databaseSearch":databaseSearch, "searchedTerm":searchDatabase})

def result(request, id=None):
    vaseObject = "No Vase Found"
    if id is not None:
        try:
            vaseObject = Vase.objects.get(vaseId=id)
        except:
            raise Http404
    return render(request, 'result.html', {"vaseObject":vaseObject})

def loginp(request):
    if request.method == "POST":
        username = request.POST.get['username']
        password = request.POST.get['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
        # login(request, user)
            return render(request, 'login.html', {})
        else:
            render(request, 'home.html', {})
