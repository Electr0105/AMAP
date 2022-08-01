from django.shortcuts import render
import sqlite3
from .models import Vase
con = sqlite3.connect('db.sqlite3',check_same_thread=False)
cur = con.cursor()
# Create your views here.
def home(request):
    if request.method == "POST":
        vaseRef = request.POST.get("vaseRef","")
        print(vaseRef)
        collectionName = request.POST.get("collectionName","")
        params = (vaseRef, collectionName)
        cur.execute("INSERT INTO website_vase (vaseRef, collectionName) VALUES (?, ?)", params)
        con.commit()
    objects = Vase.objects.all()
    return render(request, 'home.html', {'all':objects})
