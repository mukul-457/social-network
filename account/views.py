from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import forms 
from .models import Profile
from .forms import UserEditForm , ProfileEditForm
from django.contrib import messages

# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': "dashboard"})

@login_required
def profile(request):
    return HttpResponse("You are at your profile page")
        

def register(request):
    if request.method == "POST":
        register_form = forms.UserRegistrationForm(request.POST)
        if register_form.is_valid():
            cd = register_form.cleaned_data
            new_user = register_form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.save()
            profile = Profile()
            profile.user = new_user
            profile.save()
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        register_form = forms.UserRegistrationForm()
    
    return render(request, "account/register.html", {"form" : register_form})


@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(instance= request.user , data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data =request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "profile updated successfully")
        else:
            messages.error(request, "Error updating the profile")
    else:
        user_form = UserEditForm(instance= request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request, "account/edit.html", {"user_form": user_form, "profile_form": profile_form})

