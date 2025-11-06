from django import forms
from viewer.models import Cinema
class ProfileForm(forms.Form):

    # Add your profile form fields here

    pass
class CinemaForm(forms.ModelForm):

    class Meta:

        model = Cinema

        fields = '__all__'

