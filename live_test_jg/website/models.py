from django.db import models

# Create your models here.
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
        output = "VASEID: " + str(self.vaseId) + " VASEREF: " + str(self.vaseRef) + " COLLECTIOsN NAME: " + self.collectionName
        return output