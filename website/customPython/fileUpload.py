from django.shortcuts import render
from django.db.models import Q
from django.db.models import CharField
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def convertInputFile(file):
    file = file.read()
    fileValue = file.decode('utf-8') #decode to go from Bytes to String
    return fileValue