#This file instantiates models(tables) and their attributes and initialises object-relational database
from django.db import models;
from django.db.models.fields.related import ManyToManyField;

#define vase class
class Vase(models.Model):
    vaseRef = models.AutoField(primary_key=True)
    collectionName = models.CharField(max_length=600,blank=True,null=True)
    previousColl = models.CharField(max_length=600,blank=True, null=True)
    provenanceName = models.CharField(max_length=600,blank=True,null=True)
    height = models.CharField(max_length=50,blank=True,null=True)
    diameter = models.CharField(max_length=50,blank=True,null=True)
    publications = models.CharField(max_length=700,blank=True,null=True)
    subject = models.CharField(max_length=1000,blank=True,null=True)
    fabric = models.CharField(max_length=50, blank=True,null=True)
    technique = models.CharField(max_length=50,blank=True,null=True)
    shapeName = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        output = ""
        test = ""
        if self.vaseRef is not None:
            output += "Vase Ref: " + str(self.vaseRef)
        else: output +="N/A"
        if self.collectionName is not None:
            output += " Collection Name: " + self.collectionName
        else: output +=" N/A"

        # for x in self._meta.get_fields():
        #      output += str(x)[13:] + " "
             # test = exec(self.output)
        # for x in output:
        #         field_object = self._meta.get_field(x[13:])
        #         field_value = field_object.value_from_object(self)
        #         test += field_value
        return output
