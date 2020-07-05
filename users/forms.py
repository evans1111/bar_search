from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Account

class UserRegisterForm(UserCreationForm):
    # Set EmailField(required=false) to not have it be required
    email = forms.EmailField()

    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User 
        fields = ['username', 'email']

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['image']