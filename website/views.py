from re import L
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
# from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from Spacy.loadSpacy import spacy_run, filler
from TextExtraction.text_ex import text_extractor
from TextExtraction.extraction import ref_extractor
import recordextraction
from search_scripts import search_func
from search_scripts import general_search
from .models import Vase, Archive
from django.core.files.uploadedfile import UploadedFile
from .forms import UploadFileForm
from .forms import ArchiveForm
from django.http import Http404, HttpResponseRedirect
from django.http import JsonResponse
from sql_scripts import insert_to_DB, modify_record, delete_record
from .forms import UploadFileForm
from django.core.files.storage import default_storage
from zipfile import ZipFile

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

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

@login_required
def upload(request):
    """Renders the upload page"""
    return render(request, 'upload.html', {})

def contact(request):
    """Renders the contact page"""
    return render(request, 'contact.html', {})

def about(request):
    """Renders the about page"""
    return render(request, 'about.html', {})

@login_required
def upload_file(request):
    """Renders the upload_file page"""
    if request.method == 'POST' and request.FILES['myfile']:
        my_file = request.FILES['myfile']
        ref_extractor(my_file)
        return redirect(database)
    else:
        return render(request, 'upload_file.html', {})

@login_required
def upload_pdf(request):
    """Renders the upload_pdf page"""
    if request.method == 'POST':
        form = ArchiveForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/files")
    
    else:
        form = ArchiveForm()
        return render(request, "upload_pdf.html", {"form": form})

@login_required
def files(request):
    """Renders the files page"""
    objects = Archive.objects.all()
    archives = []
    for archive in objects:
        archives.append(archive.all_values_culled())
    return render(request, 'files.html', {"archives": archives})

@login_required
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
            insert_to_DB(vase_values)
            return redirect(database)
        else:
            return render(request, 'upload_text.html', {})
    else:
        return render(request, 'upload_text.html', {})

def upload_confirm(request):
    """Renders the upload_file page"""
    if request.method == "POST":
        if 'confirm' in request.POST:
            print("CONFIRM")
        elif 'cancel' in request.POST:
            print("CANCEL")
    return render(request, 'upload_confirm.html', {})

def upload_edits(request):
    """Renders the upload_file page"""
    return render(request, 'upload_edits.html', {})

@login_required
def database(request):
    """Renders the database page"""
    objects = Vase.objects.all()
    all_vases = []
    for vase_object in objects:
        all_vases.append(vase_object.all_values_culled())
    return render(request, 'database.html', {"all_vases": all_vases})

def advanced_search(request):
    """Renders the search page"""
    search_values = {}
    if request.method =="POST" and 'search' in request.POST:
        for value in request.POST:
            if value.isupper() and request.POST.get(value) != "":
                search_values.update({value:request.POST.get(value)})
        search_results = search_func(search_values)
        return render(request, "search_result.html", {"search_results":search_results})
    else:
        return render(request, 'advanced_search.html', {})

def search_result(request):
    """Renders the search_result page"""
    if request.method == "POST":
        search_value = request.POST.get("search")
        search_results = general_search(search_value)
        return render(request, 'search_result.html', {"search_results":search_results})
    else:
        return render(request, 'search_result.html', {})

def vase_page(request, id=None):
    """Renders vase page"""
    if id is not None:
        if 'save' in request.POST:
            vase_values = {}
            for value in request.POST:
                if value.isupper():
                    vase_values.update({value:request.POST.get(value)})
            modify_record(id, vase_values)
            return redirect(database)
        elif 'delete' in request.POST:
            delete_record(id)
            return redirect(database)
        else:
            try:
                vase_object = Vase.objects.get(VASEID=id)
                vase_output = vase_object.all_values_culled()
                return render(request, 'vase.html', {"vase_object":vase_object, "vase_output":vase_output, "vase_id":id})
            except:
                return render(request, 'missing_vase.html', {})
    else:
        return render(request, 'database.html', {})

def spacy_page(request):
    """Renders spacy page"""
    if request.method == "POST":
        print(file.read())
        return render(request, 'spacy.html', {})
    return render(request, 'spacy.html', {})