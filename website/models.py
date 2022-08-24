from django.db import models
from django.forms.models import model_to_dict
# Create your models here.
class Vase(models.Model):
    VASEID = models.AutoField(primary_key=True)
    VASEREF = models.CharField(max_length=16, blank=True, null=True)
    COLLECTION = models.CharField(max_length=600,blank=False,null=False)
    PREVIOUSCOL = models.CharField(max_length=600,blank=True, null=True)
    DESCRIPTION = models.CharField(max_length=500,blank=True,null=True)
    provenance_name = models.CharField(max_length=600,blank=True,null=True)
    HEIGHT = models.CharField(max_length=50,blank=True,null=True)
    DIAMETER = models.CharField(max_length=50,blank=True,null=True)
    PUBLICATION = models.CharField(max_length=300,blank=True,null=True)
    PLATE = models.CharField(max_length=100, blank=True,null=True)
    FABRIC = models.CharField(max_length=50, blank=True,null=True)
    TECHNIQUE = models.CharField(max_length=50,blank=True,null=True)
    SHAPE = models.CharField(max_length=50,blank=True,null=True)
    
    def __str__(self):
        output = "VASEID: " + str(self.VASEID) + " VASEREF: " + str(self.VASEREF) + " COLLECTION NAME: " + self.COLLECTION
        return output

    def all_fields(self):
        fields = []
        for field in Vase._meta.get_fields():
            fields.append(str(field).replace("website.Vase.", ""))
        return fields

    def all_values(self):
        output = model_to_dict(self)
        return output

    def all_values_culled(self):
        output = model_to_dict(self)
        culled_dict = {key:val for key, val in output.items() if val is not None}
        return culled_dict