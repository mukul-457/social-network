from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password  = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="password" , widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ["username", "first_name", "email"]
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError("password doesn't match")
        return cd['password2']
    
    def clean_email(self):
        cd  = self.cleaned_data
        if User.objects.filter(email = cd['email']).exists():
            raise ValidationError("Email already in use")
        return cd['email']
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
    def clean_email(self):
        cd = self.cleaned_data
        qs = User.objects.exclude(id=self.instance.id).filter(email=cd['email'])
        if qs.exists():
            raise ValidationError("Email already in use")
        return cd['email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'image']
