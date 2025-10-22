from django.shortcuts import render, redirect
from .forms import UserForm, ProfileForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import EditProfileForm, EditPasswordForm
from django.contrib import messages

# Create your views here.
def acceuil(request):# affiche la page d'accueil
    return render(request, 'utilisateurs/index.html')

def register(request):#  gere l inscription du  user
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)  # Don't save the user yet
            user.set_password(user_form.cleaned_data.get('password1'))  # Set the password correctly
            user.save()  # Now save the user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            messages.success(request, 'Votre inscription a été reçue. Un administrateur doit approuver votre compte si vous êtes un tuteur.')
            return HttpResponseRedirect(reverse('login'))
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    content = {
        'registered': registered,
        'form1': user_form,
        'form2': profile_form,
    }
    return render(request, 'utilisateurs/register.html', content)

def user_login(request):#gere la connexion de uer
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                profile = user.profile
                if not profile.is_approved and profile.type_profil == 'enseignant':
                    return HttpResponse("Votre compte enseignant doit être approuvé par un administrateur.")
                login(request, user)
                if user.is_superuser:
                    # Redirection vers la page d'administration de Django
                    return HttpResponseRedirect(reverse('admin:index'))
                else:
                    return HttpResponseRedirect('/')
            else:
                return HttpResponse("L'utilisateur est désactivé")
        else:
            return HttpResponse("Nom ou mot de passe incorrecte")
    else:
        return render(request, 'utilisateurs/login.html')

@login_required
def user_logout(request):# gere la deconnexion user
    logout(request)
    return HttpResponseRedirect('/') 

@login_required
def edit_profile(request):# gere la modification des infos du profil
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('acceuil')  # Rediriger vers la page d'accueil
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'utilisateurs/edit_profile.html', {'form': form})

@login_required
def change_password(request):# chaanger le mdp user
    if request.method == 'POST':
        form = EditPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important pour que l'utilisateur reste connecté après avoir changé son mot de passe
            return redirect('acceuil')  # Rediriger vers la page d'accueil
    else:
        form = EditPasswordForm(request.user)
    return render(request, 'utilisateurs/change_password.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'utilisateurs/profile.html')
