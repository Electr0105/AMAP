import sqlite3
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from django.contrib import messages
from Spacy.loadSpacy import spacy_run
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
    return render(request, 'home.html', {'all':objects})

def loginUser(request):
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
                # Redirect to a success page.
                return redirect('/')
            else:
                messages.success(request, "Login failed, please try again")
                return redirect('/login')
        else:
            return render(request, 'login.html', {})

def upload(request):
    """Renders the upload page"""
    # if request.method == "POST":
    #     if 'refresh' in request.POST:
    #         return render(request, 'upload.html', {})
        
    #     elif 'input_string' in request.POST:
    #         input_string = request.POST.get('input_string')
    #         print(input_string)
    #         if input_string:
    #             output_string = spacy_run(input_string)
    #             return render(request, 'upload.html', {"output_string":output_string})
    #         else:
    #             return render(request, 'upload.html', {})
        
    #     elif 'docfile' in request.POST:
    #         if request.FILES['docfile'] is not None:
    #             file = request.FILES['docfile']
    #             return render(request, 'upload.html', {"file_name": file})
    #         else:
    #             return render(request, 'upload.html', {})
        
    #     else:
    #         return render(request, 'upload.html', {})
    # else:
    return render(request, 'upload.html', {})
    # if request.POST.get("refresh"):
    #     request.FILES['docfile'] = None

    # elif request.POST.get('input_string') is not None:
    #     input_string = request.POST.get('input_string')
    #     if input_string:
    #         output_string = spacy_run(input_string)
    #         return render(request, 'upload.html', {"output_string":output_string})
    # elif request.FILES['docfile']:
    #     print("TEST32: " + str(request.FILES['docfile']))
    #     file = request.FILES['docfile']
    #     file_name = file.name
    #     print(file_name)
    #     return render(request, 'upload.html', {"file_name": file})
    # else:
    #     return render(request, 'upload.html', {})

    # if request.method == "POST":
    #     if len(request.FILES) == 1:
    #         file_value = request.FILES["docfile"].read().decode('UTF-8')
    #         # f = open("demofile3.txt", "w")
    #         # f.write(file_value)
    #         # f.close()
    #         return render(request, 'upload.html', {"value":file_value})
    #     else:
    #         output_string_form = OutputForm(request.POST)
    #         if output_string_form.is_valid():
    #             text_value = request.GET.get("text_value","Default")
    #             print(text_value)
    #             return render(request, 'upload.html', {"text_value":text_value})
    #         else:
    #             output_string_form = OutputForm()
    #         return render(request, 'upload.html', {"output_string_form":output_string_form})
    # else:
    #     return render(request, 'upload.html', {})

def about(request):
    """Renders the about page"""
    return render(request, 'home.html', {})

def upload_file(request):
    """Renders the upload_file page"""
    return render(request, 'upload_file.html', {})

def upload_text(request):
    """Renders the upload_file page"""
    if request.method == "POST":
        output_string = request.POST.get("input_string")
        print(output_string)
        spacy_string = spacy_run(output_string)
        return render(request, 'upload_text.html', {"output_string":output_string, "spacy_string":spacy_string})
    else:
        return render(request, 'upload_text.html', {})