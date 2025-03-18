from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    pin = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = User
        fields = ['name']

class LoginForm(forms.Form):
    name = forms.CharField(max_length=100)
    pin = forms.CharField(widget=forms.HiddenInput())

