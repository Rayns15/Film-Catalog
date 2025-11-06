from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Movie, Cinema, Profile
from .forms import ProfileForm, CinemaForm

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


# def afiseaza_home_page(request):
#     query = request.GET.get('q', '')
#     if query:
#         movies = Movie.objects.filter(title__icontains=query)
#     else:
#         movies = Movie.objects.all()
#     return render(request, 'home.html', {'movies': movies, 'query': query})

# class MovieDetailView(DetailView):
#     model = Movie
#     template_name = 'movie_detail.html'
#     context_object_name = 'movie'

# class MovieCreateView(LoginRequiredMixin, CreateView):
#     model = Movie
#     fields = ['title', 'description', 'release_date', 'genre']
#     template_name = 'movie_form.html'
#     success_url = reverse_lazy('home')

# class MovieUpdateView(LoginRequiredMixin, UpdateView):
#     model = Movie
#     fields = ['title', 'description', 'release_date', 'genre']
#     template_name = 'movie_form.html'
#     success_url = reverse_lazy('home')

# class MovieDeleteView(LoginRequiredMixin, DeleteView):
#     model = Movie
#     template_name = 'movie_confirm_delete.html'
#     success_url = reverse_lazy('home')

# def cinema_prices_view(request, movie_id):
#     movie = get_object_or_404(Movie, pk=movie_id)
#     cinemas = Cinema.objects.filter(movie=movie)
#     return render(request, 'cinema_prices.html', {'movie': movie, 'cinemas': cinemas})

# class CinemaUpdateView(LoginRequiredMixin, UpdateView):
#     model = Cinema
#     form_class = CinemaForm
#     template_name = 'cinema_form.html'
    
#     def get_success_url(self):
#         return reverse_lazy('cinema_prices', kwargs={'movie_id': self.object.movie.id})

# def signup_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})

# @login_required
# def profile_view(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)
#     return render(request, 'profile.html', {'profile': profile})

# @login_required
# def edit_profile(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = ProfileForm(instance=profile)
#     return render(request, 'profile_edit.html', {'form': form})

# @login_required
# def profile_delete_view(request):
#     if request.method == 'POST':
#         request.user.delete()
#         return redirect('home')
#     return render(request, 'profile_delete.html')

# def chat_api(request):
#     message = request.GET.get('message', '')
#     response = f"Echo: {message}"
#     return JsonResponse({'response': response})