from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            Profile.objects.create(
                user=user,
                telefon=self.cleaned_data['telefon']
            )
        return user
    

# class ProfileForm(forms.Form):
#     # Define your fields here, for example:
#     first_name = forms.CharField(max_length=30)
#     last_name = forms.CharField(max_length=30)
#     email = forms.EmailField()

# In your app's forms.py (e.g., accounts/forms.py)

# Define the CSS class string for styling inputs (optional but recommended)
# In forms.py

input_css_class = "w-full p-3 rounded-lg border border-[rgba(255,255,255,0.25)] bg-[rgba(13,18,38,0.35)] text-white outline-none transition-all focus:border-[#a78bfa] focus:shadow-[0_0_0_4px_rgba(167,139,250,0.25)] focus:bg-[rgba(13,18,38,0.5)] h-[44px] text-[15px]"

class CustomSignupForm(UserCreationForm):
    # Keep email definition
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': input_css_class,
        'placeholder': 'Email Address',
        'autocomplete': 'email' # Added autocomplete
    }))
    # Keep username definition (it overrides the default UserCreationForm one)
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': input_css_class,
        'placeholder': 'Username',
        'autocomplete': 'username' # Added autocomplete
    }))

    # --- ADD first_name and last_name ---
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
    # --- END ADD ---

    # Keep password definitions (overriding UserCreationForm ones to add styling)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': input_css_class,
        'placeholder': 'Password',
        'autocomplete': 'new-password' # Added autocomplete
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': input_css_class,
        'placeholder': 'Confirm Password',
        'autocomplete': 'new-password' # Added autocomplete
    }))

    class Meta:
        model = User
        # Update fields to include first_name and last_name
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2') # No need for password fields here, UserCreationForm handles them

    def save(self, commit=True):
        user = super().save(commit=False)
        # Ensure email, first_name, and last_name are saved
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '') # Use .get for optional fields
        user.last_name = self.cleaned_data.get('last_name', '') # Use .get for optional fields
        if commit:
            user.save()
        return user

class ProfileForm(forms.Form):
    # Define your fields here, for example:
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

