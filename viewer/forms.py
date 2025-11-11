from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Movie, Profile, Cinema, Showtime, ChatMessage

# --- Form for Showtime Scheduler ---
class ShowtimeForm(forms.ModelForm):
    class Meta:
        model = Showtime
        fields = ['movie', 'cinema', 'show_time']
        widgets = {
            'movie': forms.Select(attrs={'class': 'form-control'}),
            'cinema': forms.Select(attrs={'class': 'form-control'}),
            'show_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sortează listele dropdown pentru a fi mai ușor de folosit
        self.fields['movie'].queryset = Movie.objects.all().order_by('title')
        self.fields['cinema'].queryset = Cinema.objects.all().order_by('name')

# --- Form for Cinema Price Updates ---
class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = [
            'name', 'location', 
            'Adult_ticket_price', 'Child_ticket_price', 'Senior_ticket_price', 'Student_ticket_price',
            'weekend_surcharge', 'holiday_surcharge', 'weekday_discount', 'matinee_discount'
        ]

# --- Form for Movie Create/Update ---
# (This was moved from views.py)
_MOVIE_FIELD_NAMES = {f.name for f in Movie._meta.get_fields()}
_GENRE_FIELD = 'genre_movie' if 'genre_movie' in _MOVIE_FIELD_NAMES else ('genre' if 'genre' in _MOVIE_FIELD_NAMES else None)
_BASE_FIELDS = ['title', 'director', 'year', 'rating', 'genre_movie', 'bio', 'profile_picture', 'cinema_price']
_FORM_FIELDS = _BASE_FIELDS + ([_GENRE_FIELD] if _GENRE_FIELD and _GENRE_FIELD not in _BASE_FIELDS else [])

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = _FORM_FIELDS

# --- Styling for Auth Forms ---
input_css_class = "w-full p-3 rounded-lg border border-[rgba(255,255,255,0.25)] bg-[rgba(13,18,38,0.35)] text-white outline-none transition-all focus:border-[#a78bfa] focus:shadow-[0_0_0_4px_rgba(167,139,250,0.25)] focus:bg-[rgba(13,18,38,0.5)] h-[44px] text-[15px]"

# --- Main Signup Form ---
class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': input_css_class,
        'placeholder': 'Email Address',
        'autocomplete': 'email'
    }))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': input_css_class,
        'placeholder': 'Username',
        'autocomplete': 'username'
    }))
    first_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={
        'class': input_css_class,
        'placeholder': 'First Name (Optional)',
        'autocomplete': 'given-name'
    }))
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={
        'class': input_css_class,
        'placeholder': 'Last Name (Optional)',
        'autocomplete': 'family-name'
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': input_css_class,
        'placeholder': 'Password',
        'autocomplete': 'new-password'
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': input_css_class,
        'placeholder': 'Confirm Password',
        'autocomplete': 'new-password'
    }))

    class Meta:
        model = User
        # This is the correct field list
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user

# --- Old/Unused RegisterForm (FIXED) ---
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        # This was the first error: You had two Meta classes. This is the correct one.
        fields = ['username', 'first_name', 'last_name', 'email'] # Removed 'password1'/'password2'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # This was the second error: 'telefon' was not defined.
            # I have commented it out.
            # Profile.objects.create(
            #     user=user,
            #     # telefon=self.cleaned_data['telefon'] 
            # )
        return user

# --- Simple Profile Form ---
class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()