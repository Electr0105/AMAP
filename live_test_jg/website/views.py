import sqlite3
from textwrap import fill
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from Spacy.loadSpacy import spacy_run, filler
from TextExtraction.text_ex import text_extractor
from .models import Vase
from django.core.files.uploadedfile import UploadedFile
from .forms import UploadFileForm


con = sqlite3.connect('db.sqlite3', check_same_thread=False)
cur = con.cursor()


# Create your views here.
def home(request):
    if request.method == "POST":
        vase_ref = request.POST.get("vase_ref","")
        collection_name = request.POST.get("collection_name","")
        params = (vase_ref, collection_name)
        cur.execute("INSERT INTO website_vase (vase_ref, collection_name) VALUES (?, ?)", params)
        con.commit()
    objects = Vase.objects.all()
    output = []
    for vase_object in objects:
        output.append(vase_object.all_values())
    return render(request, 'home.html', {'all':objects})

def login_user(request):
    """Function printing python version."""
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
                # Redirect to home page
                return redirect('/')
            else:
                messages.success(request, "Login failed, please try again")
                return redirect('/login')
        else:
            return render(request, 'login.html', {})

def upload(request):
    """Renders the upload page"""
    return render(request, 'upload.html', {})

def contact(request):
    """Renders the contact page"""
    return render(request, 'contact.html', {})

def about(request):
    """Renders the about page"""
    return render(request, 'home.html', {})

def upload_file(request):
    """Renders the upload_file page"""
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        text = text_extractor(myfile)
        print(text)
        return render(request, 'upload_file.html', {"uploaded_file_url":uploaded_file_url, "text":text})
    else:
        return render(request, 'upload_file.html', {})

def upload_text(request):
    """Renders the upload_file page"""
    if request.method == "POST":
        vase = Vase()
        all_fields = vase.all_values()
        input_string = request.POST.get("input_string")
        spacy_string = spacy_run(input_string)
        output_dict = dict(zip(spacy_string, all_fields))
        test_string = filler(spacy_string)
        return render(request, 'upload_confirm.html', {"test_string":test_string,"input_string":input_string, "spacy_string":spacy_string, "output_dict":output_dict})
    else:
        return render(request, 'upload_text.html', {})

def upload_confirm(request):
    """Renders the upload_file page"""
    return render(request, 'upload_confirm.html', {})

def upload_edits(request):
    """Renders the upload_file page"""
    return render(request, 'upload_edits.html', {})

def database(request):
    """Renders the database page"""
    objects = Vase.objects.all()
    all_vases = []
    for vase_object in objects:
        all_vases.append(vase_object.all_values_culled())
    return render(request, 'database.html', {"all_vases": all_vases})

def search(request):
    """Renders the search page"""
    return render(request, 'search.html', {})

