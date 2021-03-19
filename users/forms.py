from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from django.views.generic import ListView
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    user_git_id = models.CharField(max_length=100)
    user_redmine = models.CharField(max_length=100)
    #password1 = forms.CharField(widget=forms.PasswordInput)
    #password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']
        user_git_id = models.CharField(max_length=100)
        user_redmine = models.CharField(max_length=100)

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    user_git_id = models.CharField(max_length=100)
    user_redmine = models.CharField(max_length=100)
   
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']
        user_git_id = models.CharField(max_length=100)
        user_redmine = models.CharField(max_length=100)
  
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
                 'email',
                 'first_name'    
                )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

