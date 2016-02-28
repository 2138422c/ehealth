from django import forms
from django.contrib.auth.models import User
from fhsa.models import UserProfile, UserFolder

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'gender', 'DOB',)

class UserFolderForm(forms.ModelForm):
    class Meta:
        model = UserFolder
        fields = ('name', 'description', 'user')