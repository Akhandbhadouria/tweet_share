from django import forms
from .models import Tweet

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class TweetForm(forms.ModelForm):
    class Meta:
        model=Tweet
        fields=['text','photo']

# class UserRegrestrationForm(UserCreationForm):
#     email=forms.EmailField()
#     class Meta:
#         model=User
#         fields=('username','email','password1','password2')


class UserRegrestrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-input'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-input'}))

    class Meta:
        model = User
        fields = ('username','email','password1','password2')


# What this does

# In Django, forms are used to collect and validate user input.
# A ModelForm automatically builds a form from your model fields, so you don’t have to write the HTML for every field manually.

# Here:
# model = Tweet → The form is linked to your Tweet model.
# fields = ['text', 'photo'] → Only these two fields will show in the form (not user or updated_at, since those are handled automatically).