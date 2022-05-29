#This file instantiates models(tables) and their attributes and initialises object-relational database
from django.db import models
# from django.db.models.fields.related import ManyToManyField

#define vase class
class Vase(models.Model):
    vaseId = models.AutoField(primary_key=True)
    vaseRef = models.CharField(max_length=16, blank=True, null=True)
    collectionName = models.CharField(max_length=600,blank=False,null=False)
    previousColl = models.CharField(max_length=600,blank=True, null=True)
    description = models.CharField(max_length=500,blank=True,null=True)
    provenanceName = models.CharField(max_length=600,blank=True,null=True)
    height = models.CharField(max_length=50,blank=True,null=True)
    diameter = models.CharField(max_length=50,blank=True,null=True)
    publications = models.CharField(max_length=300,blank=True,null=True)
    plateId = models.CharField(max_length=100, blank=True,null=True)
    fabric = models.CharField(max_length=50, blank=True,null=True)
    technique = models.CharField(max_length=50,blank=True,null=True)
    shapeName = models.CharField(max_length=50,blank=True,null=True)
    

    def __str__(self):
        output = ""
        if self.vaseId is not None:
            output += "Vase ID: " + str(self.vaseId)
        else: output +="N/A"
        if self.vaseRef is not None:
            output += " Vase Ref: " + str(self.vaseRef)
        else: output +="N/A"
        if self.collectionName is not None:
            output += " Collection Name: " + self.collectionName
        else: output +=" N/A"
        if self.provenanceName is not None:
            output += " Provenance Name: " + self.provenanceName
        else: output +=" N/A"

        # for x in self._meta.get_fields():
        #      output += str(x)[13:] + " "
             # test = exec(self.output)
        # for x in output:
        #         field_object = self._meta.get_field(x[13:])
        #         field_value = field_object.value_from_object(self)
        #         test += field_value
        return output

class Plate(models.Model):
    plateId = models.CharField(max_length=100, primary_key=True)
    imageRef = models.CharField(max_length=500, blank=True,null=True)

    def __str__(self):
        output = ""
        if self.plateId is not None:
            output += "Plate ID: " + str(self.plateId)
        else: output +="N/A"
        if self.imageRef is not None:
            output += "Image Ref: " + self.imageRef
        else: output +=" N/A"