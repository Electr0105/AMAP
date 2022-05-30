from django.shortcuts import render
from django.db.models import Q
from django.db.models import CharField
from django.conf import settings
from dbdisplay.website.models import Vase

def searchDatabase(term):
    for x in Vase._meta.fields:
        print(x)