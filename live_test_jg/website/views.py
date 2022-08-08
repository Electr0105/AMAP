from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import sqlite3
from .models import Vase
from django.contrib.auth.models import User
con = sqlite3.connect('db.sqlite3', check_same_thread=False)
cur = con.cursor()
# Create your views here.
def home(request):
    if request.method == "POST":
        vaseRef = request.POST.get("vaseRef","")
        collectionName = request.POST.get("collectionName","")
        params = (vaseRef, collectionName)
        cur.execute("INSERT INTO website_vase (vaseRef, collectionName) VALUES (?, ?)", params)
        con.commit()
    objects = Vase.objects.all()
    return render(request, 'home.html', {'all':objects})

def loginUser(request):
    if request.user.is_authenticated:
        print(request.user)
        logout(request)
        messages.success(request, "You've been logged out")
        return redirect('/login')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('/')
            else:
                messages.success(request, "Login failed, please try again")
                return redirect('/login')
        else:
            return render(request, 'login.html', {})

def upload(request):
    if len(request.FILES) != 0:
        if request.method == "POST":
            fileValue = request.FILES["docfile"].read().decode('UTF-8')
            # f = open("demofile3.txt", "w")
            # f.write(fileValue)
            # f.close()
            return render(request, 'upload.html', {"value":fileValue})
        else:
            return render(request, 'upload.html', {})
    else:
        return render(request, 'upload.html', {})

def about(request):
    return render(request, 'home.html', {})