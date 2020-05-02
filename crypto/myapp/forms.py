# from django import forms


# class imageForm(forms.Form):
#     image = forms.ImageField(required=False)
from django import forms 
from .models import *
  
class HotelForm(forms.ModelForm): 
  
    class Meta: 
        model = Hotel 
        fields = ['message','key','image'] 