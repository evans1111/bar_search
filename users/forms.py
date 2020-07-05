from django import forms
from django.contrib.auth.models import User
from django.contrib.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    # Set EmailField(required=false) to not have it be required
    email = forms.EmailField()

    class Meta:
        model = User 
        fields = ['username', 'email' 'password2', 'password2']