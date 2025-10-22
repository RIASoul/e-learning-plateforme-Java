from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

class UserForm(UserCreationForm):# gerer la creation d un nouvel user
    class Meta():
        model = User
        fields=[
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',

        ]

class ProfileForm(forms.ModelForm):#gere les infos supplementaire du profil user
    class Meta():
        model = Profile
        fields=[
            'bio',
            'photo_profile',
            'type_profil',
        ]



class EditProfileForm(UserChangeForm):# mettre à jour les ifos user
    password = None  # Exclure le champ mot de passe

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        

class EditPasswordForm(PasswordChangeForm):# mettre  jour les mot de pase
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']