from re import search
from website.models import Vase
from django.db.models import CharField
from django.db.models import  Q


def search_func(search_values):
    """Take dictionary and search all vases for a match"""
    positive_vases = []
    for key, value in search_values.items():
        value = f"Vase.objects.filter({key}__icontains='{value}')"
        command = f"positive_vases.append({value})"
        exec(command)
    pass_vases = []
    if len(positive_vases) > 0:
        for x in positive_vases[0]:
            pass_vases.append(x)
    else:
        pass_vases = None
    return pass_vases

def general_search(search_value):
    search_results = Vase.objects.filter(Q(COLLECTION__icontains=search_value) |
    Q(DESCRIPTION__icontains=search_value) |
    Q(DESCRIPTION__icontains=search_value) |
    Q(DIAMETER__icontains=search_value) |
    Q(FABRIC__icontains=search_value) |
    Q(HEIGHT__icontains=search_value) |
    Q(PLATE__icontains=search_value) |
    Q(PREVIOUSCOL__icontains=search_value) |
    Q(PROVENANCE_NAME__icontains=search_value) |
    Q(PUBLICATION__icontains=search_value) |
    Q(SHAPE__icontains=search_value) |
    Q(TECHNIQUE__icontains=search_value) |
    Q(VASEID__icontains=search_value) |
    Q(VASEREF__icontains=search_value))

    if len(search_results) == 0:
        search_results = None

    return(search_results)
