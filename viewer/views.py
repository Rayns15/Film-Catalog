from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth import login, authenticate
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Prefetch, Q
from django.utils import timezone
from .models import Cinema, Showtime, Movie, ChatMessage, Profile, User
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
import json
from viewer.forms import ShowtimeForm, CinemaForm, MovieForm, ProfileForm
# Register a safe 'add_class' template filter so templates don't crash if widget_tweaks isn't loaded
from django.template.defaultfilters import register as default_template_register

class ShowtimeCreateView(CreateView):
    model = Showtime
    form_class = ShowtimeForm
    template_name = 'add_showtime.html' # Or 'showtime_manager.html'
    success_url = reverse_lazy('showtime_create') # Reload the same page

    # ADD THIS METHOD
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the list of all showtimes to the context
        context['showtime_list'] = Showtime.objects.all().order_by('-show_time')
        return context

class ShowtimeUpdateView(UpdateView):
    model = Showtime
    form_class = ShowtimeForm
    template_name = 'add_showtime.html' # Or 'showtime_manager.html'
    success_url = reverse_lazy('showtime_create') # Redirect back to the main manager page

    # ADD THIS METHOD
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the list of all showtimes to the context
        context['showtime_list'] = Showtime.objects.all().order_by('-show_time')
        return context

class ShowtimeDeleteView(DeleteView):
    model = Showtime
    template_name = 'showtime_confirm_delete.html' 
    success_url = reverse_lazy('showtime_create')

@default_template_register.filter(name='add_class')
def add_class(field, css_classes):
    try:
        existing = field.field.widget.attrs.get('class', '')
        combined = f"{existing} {css_classes}".strip()
        return field.as_widget(attrs={**field.field.widget.attrs, 'class': combined})
    except Exception:
        return field

# Import all forms from forms.py
from .forms import (
    CustomSignupForm, ProfileForm, RegisterForm, 
    CinemaForm, ShowtimeForm, MovieForm,
)

# === Staff Views ===

@staff_member_required
def add_showtime_view(request):
    if request.method == 'POST':
        form = ShowtimeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Showtime successfully added!')
            return redirect('add-showtime')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ShowtimeForm()
    context = {'form': form}
    return render(request, 'add_showtime.html', context)

@staff_member_required
def cinema_prices_update(request, pk):
    cinema = get_object_or_404(Cinema, pk=pk)
    next_url = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'POST':
        form = CinemaForm(request.POST, instance=cinema)
        if form.is_valid():
            form.save()
            messages.success(request, f"Prices for '{cinema.name}' updated successfully!")
            if next_url:
                return redirect(next_url)
            else:
                return redirect('cinema-list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CinemaForm(instance=cinema)

    context = {
        'form': form,
        'cinema': cinema,
        'next_url': next_url
    }
    return render(request, 'cinema_prices_update.html', context)

# === Chat/API Views ===

@login_required
@require_POST
def delete_chat_message(request, message_pk):
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Not authorized'}, status=403)
    try:
        message = ChatMessage.objects.get(pk=message_pk)
        message.delete()
        return JsonResponse({'status': 'ok'})
    except ChatMessage.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Message not found'}, status=404)

# This is the CORRECT version of post_chat_message
@login_required
@require_POST
def post_chat_message(request, movie_pk):
    try:
        movie = Movie.objects.get(pk=movie_pk)
        data = json.loads(request.body)
        message_text = data.get('message')

        if not message_text:
            return JsonResponse({'status': 'error', 'message': 'Message is empty'}, status=400)

        chat_message = ChatMessage.objects.create(
            movie=movie,
            user=request.user,
            message=message_text
        )
        
        return JsonResponse({
            'status': 'ok',
            'message': chat_message.message,
            'user': chat_message.user.username,
            'timestamp': chat_message.timestamp.strftime('%b %d, %I:%M %p'),
            'message_id': chat_message.pk  # <-- This was missing in your duplicate
        })
    except Movie.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Movie not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def chat_api(request):
    return HttpResponse("Chat API is working!")

# === Main Page Views ===

def movie_list(request):
    query = request.GET.get('q')
    no_results = False
    
    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(director__icontains=query) |
            Q(genre_movie__icontains=query)
        ).order_by('pk')
        if not movies.exists():
            no_results = True
    else:
        movies = Movie.objects.all().order_by('pk')

    context = {
        'movies_html': movies,
        'query': query,
        'no_results': no_results
    }
    return render(request, 'movie_list.html', context)

def movie_search_view(request):
    query = request.GET.get('q', '') 
    if query:
        movies = Movie.objects.filter(title__icontains=query)
        no_results = not movies.exists()
    else:
        movies = Movie.objects.none() 
        no_results = False

    return render(request, 'movie_search.html', {
        'movies_html': movies,
        'user': request.user,
        'year': datetime.datetime.now().year,
        'query': query,
        'no_results': no_results,
    })

def cinema_list_view(request):
    cinemas = Cinema.objects.all()
    context = {'cinemas': cinemas}
    return render(request, 'cinema_list.html', context)

# === Class-Based Views (CBVs) ===

class cinema_prices(DetailView):
    model = Movie
    template_name = 'cinema_prices.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        now = timezone.now()

        showtimes_for_this_movie = Prefetch(
            'cinema_showtimes',
            queryset=Showtime.objects.filter(
                movie_id=movie.pk,
                #show_time__gte=now
            ).order_by('show_time'),
            to_attr='filtered_showtimes'
        )
        
        cinemas_with_showtimes = Cinema.objects.filter(
            cinema_showtimes__movie_id=movie.pk,
            cinema_showtimes__show_time__gte=now
        ).distinct().prefetch_related(showtimes_for_this_movie)
        
        context['cinemas_with_showtimes'] = cinemas_with_showtimes
        context['chat_messages'] = ChatMessage.objects.filter(movie=movie)
        return context

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

class MovieDetailView(DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'movie_detail.html'

# === Auth & Profile Views ===

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User {user.username} signed up successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomSignupForm()
    return render(request, 'sign_up.html', {'form': form})

# This is the active profile_view linked in your urls.py
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST) # This form is simple, not a ModelForm
        if form.is_valid():
            return HttpResponse("Profile updated successfully")
    else:
        form = ProfileForm()
    return render(request, 'profile.html', {'form': form})

# This is the active edit_profile linked in your urls.py
@login_required
def edit_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user != user: # Add a check
        return redirect('home')
        
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        return redirect('profile')
    return render(request, 'profile_edit.html', {'user': user})

@login_required
def profile_delete_view(request):
    if request.method == 'POST':
        user = request.user
        user.delete() # This deletes the user
        messages.success(request, "Profile deleted successfully")
        return redirect('home')
    return render(request, 'profile_delete.html') # A confirmation page

# === Unused/Old Views (can be deleted) ===

def afiseaza_home_page(request):
    filme = Movie.objects.all()
    return render(request, 'home.html', {'movies_html': filme})

@staff_member_required
def cinema_add_view(request):
    if request.method == 'POST':
        form = CinemaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cinema '{form.cleaned_data['name']}' added successfully!")
            return redirect('cinema-list') # Redirect back to the cinema list
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CinemaForm() # A new, blank form

    context = {
        'form': form
    }
    return render(request, 'cinema_form.html', context)



# ... other unused functions like 'phone_book', 'afiseaza', etc. ...