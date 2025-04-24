from django import forms 
from .models import Tweet
from django.contrib.auth.models import User
from django.contrib.auth.forms import  UserCreationForm
class TweetForm(forms.ModelForm):
    
    class Meta:
        model = Tweet
        fields = ['text','photo']


class UserRegistrationForm(UserCreationForm): #django builtin form
    email=forms.EmailField()
    class Meta:
        model = User
        #we are using built in table.
        fields= ['username','email','password1','password2']
        # usually give two passwsord then all authentication are automatically embeded, although modifiable

