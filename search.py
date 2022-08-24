from website.models import Vase

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