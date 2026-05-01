from django import forms
from .models import Apartment

class ApartmentForm(forms.ModelForm):
    class Meta():
        model = Apartment
        exclude = ['is_reserved']
        fields = '__all__'