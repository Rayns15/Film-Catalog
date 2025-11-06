import json
import datetime
import os
import nltk  # Added for the chatbot NLTK downloads

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q, Prefetch
from .models import Cinema, Showtime, Movie # <-- CLEANED IMPORTS
from .forms import (
    CustomSignupForm, 
    ProfileForm, 
    RegisterForm, 
    UserEditForm,
    ProfileEditForm
)
# --- Chatbot Setup ---
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from movies.models import Cinema, Showtime, Movie
from .forms import ProfileForm, CinemaForm
# import models from the app that actually defines them

# import local forms
try:
    # Ensure required NLTK data is downloaded
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('stopwords', quiet=True)

    chatbot = ChatBot('CatalogBot')
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english.greetings")
    trainer.train("chatterbot.corpus.english.conversations")
except Exception as e:
    print(f"Error initializing chatbot: {e}")
    chatbot = None

# ==================================
# === MAIN PAGE & MOVIE VIEWS ===
# ==================================

def afiseaza_home_page(request): # <-- RENAMED this from home_view to match your urls.py
    """
    Handles the main homepage and searching (by Title or Genre).
    """
    query = request.GET.get('q', '')
    genre_filter = request.GET.get('genre', '') 

    # Prefetch showtimes and their related cinemas for efficiency
    movies = Movie.objects.prefetch_related('showtimes__cinema').all()
    no_results = False

    if query:
        movies = movies.filter(Q(Title__icontains=query))
        no_results = not movies.exists()
    
    elif genre_filter:
        movies = movies.filter(Q(genre_movie__icontains=genre_filter))
        no_results = not movies.exists()

    context = {
        'movies_html': movies,
        'query': query,
        'genre_filter': genre_filter,
        'no_results': no_results
    }
    return render(request, 'home.html', context)

class MovieDetailView(DetailView):
    """
    Shows the details for a single movie.
    """
    model = Movie
    context_object_name = 'movie' 
    
    def get_template_names(self):
        # This will use 'movie_16.html' for movie 16, etc.
        # But it will NOT pass the 'cinemas' context.
        return [f'movie_{self.object.pk}.html', 'movie_detail.html']

class MovieForm(forms.ModelForm):
    """
    A simple form for creating/updating movies.
    """
    class Meta:
        model = Movie
        fields = ['Title', 'director', 'Year', 'rating', 'genre_movie']

class MovieCreateView(CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movie_form.html'
    success_url = reverse_lazy("home")

class MovieUpdateView(UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movie_update.html'
    success_url = reverse_lazy("home")

class MovieDeleteView(DeleteView):
    model = Movie
    template_name = 'movie_confirm_delete.html'
    success_url = reverse_lazy("home")

# ==================================
# === CINEMA & PRICING VIEWS ===
# ==================================

def cinema_prices_view(request, movie_id): # <-- 🔴 FATAL ERROR FIXED: Added 'movie_id'
    """
    Shows prices for ALL cinemas, but showtimes ONLY for
    the movie specified by movie_id.
    """
    
    # 1. Get the specific movie we want to see
    movie = get_object_or_404(Movie, pk=movie_id)
    
    # 2. Create a Prefetch to get ONLY the showtimes for this one movie
    showtimes_for_this_movie = Prefetch(
        'cinema_showtimes',
        queryset=Showtime.objects.filter(movie_id=movie_id).order_by('show_time'),
        to_attr='filtered_showtimes' # We'll access this new name in the template
    )

    # 3. Get all cinemas, but apply our filtered prefetch
    all_cinemas = Cinema.objects.prefetch_related(
        showtimes_for_this_movie
    ).all()
    
    context = {
        'cinemas': all_cinemas,
        'movie': movie  # Pass the specific movie to the template
    }
    return render(request, 'movie_16.html', context)


class CinemaUpdateView(UserPassesTestMixin, UpdateView):
    """
    This is the correct view for your "Update Prices" form.
    """
    model = Cinema
    fields = [
        'name', 
        'location', 
        'Adult_ticket_price', 
        'Child_ticket_price', 
        'Senior_ticket_price', 
        'Student_ticket_price', 
        'weekend_surcharge', 
        'holiday_surcharge', 
        'weekday_discount', 
        'matinee_discount'
    ]
    template_name = 'cinema_update_form.html'
    
    # This URL name must match your urls.py
    # We'll fix this in the template, not here.
    # success_url = reverse_lazy('cinema_prices') # This will fail
    
    def get_success_url(self):
        # Redirects back to the prices page for the *movie you were just on*.
        # We need the movie_id from the original request.
        # This is complex. A simple redirect to 'home' might be easier.
        return reverse_lazy('home') # Let's simplify this for now

    def test_func(self):
        """Only allows staff users to access this page."""
        return self.request.user.is_staff

# ==================================
# === USER & PROFILE VIEWS ===
# ==================================

def signup_view(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = CustomSignupForm(request.POST) # Uses your CustomSignupForm
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User {user.username} signed up successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomSignupForm()

    return render(request, 'sign_up.html', {'form': form})

@login_required
def profile_view(request):
    """
    Shows the user's profile information.
    """
    return render(request, 'profile.html') # Assumes profile.html just shows user info

@login_required
def edit_profile(request):
    """
    Allows users to edit their profile information.
    """
    User = request.user.__class__
    Profile = ProfileEditForm._meta.model  # Get the Profile model from the form

    # Ensure the user has a profile
    try:
        profile = request.user.profile
    except AttributeError:
        profile = Profile.objects.create(user=request.user)
        profile.save()

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)

    return render(request, 'profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def profile_delete_view(request):
    """
    Shows a confirmation page before deleting a user.
    """
    if request.method == 'POST':
        # User confirmed deletion
        request.user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')
    
    # Show the confirmation page
    return render(request, 'profile_delete_confirm.html')

# ==================================
# === CHATBOT API VIEW ===
# ==================================

def chat_api(request):
    """
    An API view to handle chat messages.
    """
    if chatbot is None:
        return JsonResponse({'error': 'Chatbot is not available'}, status=500)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')

            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            user_msg_lower = user_message.lower()

            if user_msg_lower.startswith('search for '):
                search_query = user_message[11:].strip()
                return JsonResponse({
                    'response': f'Okay, searching for "{search_query}"...',
                    'action': 'search',
                    'query': search_query
                })
            
            elif user_msg_lower.startswith('filter by '):
                genre_query = user_message[10:].strip()
                if genre_query.lower().startswith('genre '):
                    genre_query = genre_query[6:].strip()
                
                return JsonResponse({
                    'response': f'Okay, filtering by {genre_query} movies...',
                    'action': 'filter_genre',
                    'query': genre_query
                })
            
            else:
                bot_response = str(chatbot.get_response(user_message))
                return JsonResponse({'response': bot_response})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)