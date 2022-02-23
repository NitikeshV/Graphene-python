from django import forms
from .models import Pet

class MyForm(forms.Form):
    name = forms.CharField()


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ("name",)
