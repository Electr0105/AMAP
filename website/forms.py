from django import forms
from Spacy.loadSpacy import spacy_run
from django.forms import ModelForm

from website.models import Archive


class OutputForm(forms.Form):
    """class for generating string forms"""
    output_string = forms.CharField(label='Output Value', max_length=300)

    # def getString():
    #     for x in out
    #     return output
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class ArchiveForm(ModelForm):
    class Meta:
        model = Archive
        fields = 'name', 'media'