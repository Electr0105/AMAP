from django.shortcuts import render
from .models import Vase
from django.db.models import Q
from django.db.models import CharField

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
    # if request.method == "POST":
    #     vaseRef = request.POST.get("vaseRef","")
    #     collectionName = request.POST.get("collectionName","")
    #     objects = Vase.objects.filter(vaseRef__icontains=vaseRef, collectionName__icontains=collectionName)
    #     return render(request, 'searchResult.html', {"all":objects,"vaseRef":vaseRef})
    # else:
    #     return render(request, 'search.html')
    if request.method == "POST":
        vaseRef = request.POST.get("vaseRef","")
        collectionName = request.POST.get("collectionName","")
        provenanceName = request.POST.get("provenanceName","")
        searchDatabase = request.POST.get("searchDatabase", "")
        valueSet = [vaseRef, collectionName, provenanceName]
        nameSet = {"vaseRef":vaseRef, "collectionName":collectionName,"provenanceName":provenanceName}
        allVases = Vase.objects.all()
        sortedVases = Vase.objects.filter(vaseRef__icontains=vaseRef, collectionName__icontains=collectionName, provenanceName__icontains=provenanceName)
        if(not searchDatabase):
            if not "" in valueSet:
                return render(request, 'searchResult.html', {"all":allVases})
            else:
                return render(request, 'searchResult.html', {"sortedVases":sortedVases,"vaseRef":vaseRef, "collectionName":collectionName, "provName":provenanceName, "nameSet":nameSet})
        else:
            fields = [f for f in Vase._meta.fields if isinstance(f, CharField)]
            queries = [Q(**{f.name: searchDatabase}) for f in fields]
            qs = Q()
            for query in queries:
                qs = qs | query
            if(not vaseRef):
                databaseSearch = Vase.objects.filter(qs)
            else:
                databaseSearch = Vase.objects.filter(vaseRef, qs)
            return render(request, 'searchResult.html', {"databaseSearch":databaseSearch, "searchedTerm":searchDatabase})