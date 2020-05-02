from django.db import models

# Create your models here.
class Hotel(models.Model):
	message=models.CharField(max_length=100,default=None)
	key=models.CharField(max_length=100,default=None)
	image = models.ImageField(upload_to='images/') 

class Final(models.Model):
	image = models.ImageField(upload_to='images/') 