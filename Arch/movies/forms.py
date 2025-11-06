from django import forms
from .models import Movie
# Ensure that UserEditForm is not causing circular imports

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['Title', "director", 'Year', 'rating', 'genre_movie', 'bio', 'profile_picture']

class ProfileForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField()
    bio = forms.CharField(widget=forms.Textarea)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

class ProfileEditForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField()
    bio = forms.CharField(widget=forms.Textarea)

class UserEditForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea)

class CinemaForm(forms.Form):
    title = forms.CharField(max_length=200)
    director = forms.CharField(max_length=100)
    release_year = forms.IntegerField()
    genre = forms.CharField(max_length=100)