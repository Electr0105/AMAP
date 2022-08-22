import re
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
from django.http import Http404


con = sqlite3.connect('db.sqlite3', check_same_thread=False)
cur = con.cursor()


# Create your views here.
def home(request):
    objects = Vase.objects.all()
    all_vases = []
    for vase_object in objects:
        all_vases.append(vase_object.all_values())
    return render(request, 'home.html', {'all_vases':all_vases})

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
    return render(request, 'about.html', {})

def upload_file(request):
    """Renders the upload_file page"""
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        # text = text_extractor(myfile)
        # print(text)
        return render(request, 'upload_file.html', {"uploaded_file_url":uploaded_file_url})
        text = text_extractor(myfile)
        print(text)
        return render(request, 'upload_file.html', {"uploaded_file_url":uploaded_file_url, "text":text})

        text = text_extractor(myfile)
        print(text)
        return render(request, 'upload_file.html', {"uploaded_file_url":uploaded_file_url, "text":text})

    else:
        return render(request, 'upload_file.html', {})

def upload_text(request):
    """Renders the upload_file page"""
    if request.method == "GET":
        return render(request, "upload_text.html",{})
    if request.method == "POST":
        if request.POST.get("input_string") is not None:
            vase = Vase()
            all_fields = vase.all_values()
            input_string = request.POST.get("input_string")
            spacy_string = spacy_run(input_string)
            output_dict = dict(zip(spacy_string, all_fields))
            test_string = filler(spacy_string)
            return render(request, "upload_confirm.html", {"test_string":test_string,"input_string":input_string, "spacy_string":spacy_string, "output_dict":output_dict})
        elif 'confirm' in request.POST:
            vase_values = {}
            for value in request.POST:
                if value.isupper():
                    vase_values.update({value:request.POST.get(value)})
            string_start = "INSERT INTO website_vase ("
            string_end = ""
            for key, value in vase_values.items():
                string_start += f"{str(key)}, "
                string_end += f"\"{str(value)}\", "
            string_start = string_start[:-2] + ") VALUES ("
            string_end = string_end[:-2] + ")"
            command = string_start + string_end
            print(command)
            cur.execute(command)
            con.commit()
            return render(request, 'upload_text.html', {})
        else:
            return render(request, 'upload_text.html', {})
    else:
        return render(request, 'upload_text.html', {})

def upload_confirm(request):
    """Renders the upload_file page"""
    print("ASDDSDSDADADASD")
    if request.method == "POST":
        if 'confirm' in request.POST:
            print("CONFIRM")
        elif 'cancel' in request.POST:
            print("CANCEL")
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

def vase_page(request, id=None):
    """Renders vase page"""
    if id is not None:
        try:
            vase_object = Vase.objects.get(VASEID=id)
            vase_output = vase_object.all_values_culled()
            return render(request, 'vase.html', {"vase_object":vase_object, "vase_output":vase_output, "vase_id":id})
        except:
            return render(request, 'missing_vase.html', {})
    else:
        return render(request, 'vase.html', {})