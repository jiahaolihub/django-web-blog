from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# inherit from traditional form, added email field
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # Meta: a nested namespace configuration in one place
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] # added addition email field

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']