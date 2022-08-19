from django.db import models
from django.forms.models import model_to_dict
# Create your models here.
class Vase(models.Model):
    vase_id = models.AutoField(primary_key=True)
    vase_ref = models.CharField(max_length=16, blank=True, null=True)
    collection_name = models.CharField(max_length=600,blank=False,null=False)
    previous_coll = models.CharField(max_length=600,blank=True, null=True)
    description = models.CharField(max_length=500,blank=True,null=True)
    provenance_name = models.CharField(max_length=600,blank=True,null=True)
    height = models.CharField(max_length=50,blank=True,null=True)
    diameter = models.CharField(max_length=50,blank=True,null=True)
    publications = models.CharField(max_length=300,blank=True,null=True)
    plate_id = models.CharField(max_length=100, blank=True,null=True)
    fabric = models.CharField(max_length=50, blank=True,null=True)
    technique = models.CharField(max_length=50,blank=True,null=True)
    shape_name = models.CharField(max_length=50,blank=True,null=True)
    
    def __str__(self):
        output = "VASEID: " + str(self.vase_id) + " VASEREF: " + str(self.vase_ref) + " COLLECTION NAME: " + self.collection_name
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