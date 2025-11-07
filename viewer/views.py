from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from viewer.models import Movie, Showtime
from django.db.models import Model, IntegerField, CharField
from django.views import View
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import login, authenticate
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm # Or your custom SignupForm
from django.contrib import messages
from .forms import CustomSignupForm, ProfileForm, RegisterForm, CinemaForm
from django.db.models import Prefetch
from django.utils import timezone
from .models import Cinema, Showtime, Movie

# Create your views here.

def chat_api(request):
    return HttpResponse("Chat API is working!")

def base_view(request):
    return render(request, 'base.html')

# def search(request):
#     query = request.GET.get('q', '')
#     movies = Movie.objects.filter(Title__icontains=query)
    
#     # Check if the search returned any movies
#     no_results = not movies.exists() if query else False # Only show if a query was made

#     context = {
#         'movies_html': movies,
#         'query': query, # Pass the query back to display it
#         'no_results': no_results # Add the flag to the context
#     }
#     return render(request, 'home.html', context)
    
# nume.com/hello_regex?"nume='Andrei":
#     return HttpResponse(request):
#         nume_url = request.GET.net('nume', '')
#         return HttpResponse(f"Hello, {nume}!")

dictionary = {"Strada1": 46565, "Strada2": 651245, "Strada3": 6512452}
def phone_book(request):
    strada = request.GET.get('strada', '')
    if strada in dictionary:
        return HttpResponse(f"Phone number for {strada} is {dictionary[strada]}")
    else:
        return HttpResponse("Not found")
 
def phone_book2(request):
    strada = request.GET.get('strada', '')
    nrtelefon = int(request.GET.get('nrtelefon', 0))
    for key, value in dictionary.items():
        if key == strada:
            return HttpResponse(f"Phone number for {strada} is {value}")
        elif value == nrtelefon:
            return HttpResponse(f"Street for phone number {nrtelefon} is {key}")
    return HttpResponse("Not found")

def afiseaza(request):
    filme = Movie.objects.all()
    output = ""
    for film in filme:
        output += f"Title: {film.Title}, Director: {film.director}, Year: {film.Year}<br>" 
    return HttpResponse(output)

def show_streams(request):
    nume_url = request.GET.get('nume', '')
    prenume_url = request.GET.get('prenume', '')
    return HttpResponse(f"Hello, {nume_url} {prenume_url}!")

def afiseaza_home_page(request):
    filme = Movie.objects.all()
    return render(request, 'home.html', {'movies_html': filme})

# Build a reusable ModelForm that includes the genre field if present on the Movie model
_MOVIE_FIELD_NAMES = {f.name for f in Movie._meta.get_fields()}
_GENRE_FIELD = 'genre_movie' if 'genre_movie' in _MOVIE_FIELD_NAMES else ('genre' if 'genre' in _MOVIE_FIELD_NAMES else None)
_BASE_FIELDS = ['title', 'director', 'year', 'rating', 'genre_movie', 'bio', 'profile_picture', 'cinema_price'] # <-- Fixed
_FORM_FIELDS = _BASE_FIELDS + ([_GENRE_FIELD] if _GENRE_FIELD else [])

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = _FORM_FIELDS

class MovieCreateView(CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movie_form.html'
    success_url = reverse_lazy("home")  # Redirect to home page after successful creation

class MovieListView(ListView):
    model = Movie
    template_name = 'movie_list.html'
    context_object_name = 'movies_html'

def shawshank_redemption_view(request):
    return render(request, 'shawshank_redemption.html')

def inception_view(request):
    # Reuse the existing 'search' logic to respond for "Inception"
    return search(request, "Inception")

class MovieUpdateView(UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movie_update.html'
    success_url = reverse_lazy("home")

class MovieDeleteView(DeleteView):
    model = Movie
    template_name = 'movie_confirm_delete.html'
    success_url = reverse_lazy("home")  # Redirect to home page after successful deletion

def movie1_details(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
        return render(request, f'movie_{pk}.html', {'movie': movie})
    except Movie.DoesNotExist:
        return HttpResponse("Movie not found", status=404)

class view_details(View):
    model = Movie
    template_name = 'Inception.html'
    context_object_name = 'movie_html'
    success_url = reverse_lazy("home")  # Redirect to home page after successful creation

    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            return render(request, self.template_name, {'movie_html': movie})
        except Movie.DoesNotExist:
            return HttpResponse("Movie not found", status=404)        

class MovieDetailView(DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'movie_detail.html'  # Default template

    # def get_template_names(self):
    #     if self.object:
    #         return [f'movie_{self.object.id}.html', self.template_name]
    #     return [self.template_name]

def movie_details_view(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
        return render(request, f'movie_{pk}.html', {'movie': movie})
    except Movie.DoesNotExist:
        return HttpResponse("Movie not found", status=404)
  # Ensure the template exists

class TheGodfatherView(DetailView):
    model = Movie
    template_name = 'The Godfather.html'
    context_object_name = 'movie_html'
    success_url = reverse_lazy("home")
    def get_object(self, queryset=None):
        return Movie.objects.get(Title="The Godfather")
    # Ensure views are imported if views.py exists

def movie_details(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
        return render(request, 'movie_details.html', {'movie': movie})
    except Movie.DoesNotExist:
        return HttpResponse("Movie not found", status=404)

def the_godfather(request, slug=None):
    try:
        if slug is None:
            return HttpResponse("Slug not provided", status=400)
        movie = Movie.objects.get(slug=slug)
        return render(request, 'The Godfather.html', {'movie': movie})
    except Movie.DoesNotExist:
        return HttpResponse("Movie not found", status=404)
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
def serve_static(request, path):
    from django.conf import settings
    from django.views.static import serve
    return serve(request, path, document_root=settings.STATIC_ROOT)
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Here you would typically authenticate the user
            return HttpResponse(f"Logged in as {username}")
    else:
        form = LoginForm()
    return render(request, 'Log_in.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        # 2. Use CustomSignupForm for POST data
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User {user.username} signed up successfully!")
            # Redirect to login page after successful signup
            return redirect('login')
        else:
            # If form is invalid, errors will be shown on the template
            messages.error(request, "Please correct the errors below.")
            # No need to explicitly render here, it falls through
    else:
        # 2. Use CustomSignupForm for GET requests (blank form)
        form = CustomSignupForm()

    # Render the signup page with the form (either blank or with errors)
    # Make sure 'Sign_up.html' matches your actual template filename
    return render(request, 'sign_up.html', {'form': form})

def logout_view(request):
    # Here you would typically log out the user
    return HttpResponse("Logged out successfully")

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Here you would typically create the user
            return HttpResponse(f"User {username} signed up successfully")
    else:
        form = SignupForm()
    return render(request, 'sign_up.html', {'form': form})

def movie_search_view(request):
    query = request.GET.get('q', '') 
    
    if query:
        # --- IF there is a query, filter the movies ---
        # This is the line that actually performs the search
        movies = Movie.objects.filter(title__icontains=query)
        no_results = not movies.exists()
    else:
        # --- IF the query is empty, show no movies ---
        movies = Movie.objects.none() 
        no_results = False

    # Render the SAME 'home.html' template, but with the filtered 'movies'
    return render(request, 'home.html', {
        'movies_html': movies,
        'user': request.user,
        'year': datetime.datetime.now().year,
        'query': query,       # Pass the query back to the template
        'no_results': no_results,
    })

def movie_search(request):
    # Get the search term from the URL's 'q' parameter
    query = request.GET.get('q', '') 
    
    if query:
        # --- IF there is a query, filter the movies ---
        # This is the line that actually performs the search
        movies = Movie.objects.filter(Title__icontains=query)
        no_results = not movies.exists()
    else:
        # --- IF the query is empty, show no movies ---
        movies = Movie.objects.none() 
        no_results = False

    # Render the SAME 'home.html' template, but with the filtered 'movies'
    return render(request, 'home.html', {
        'movies_html': movies,
        'user': request.user,
        'year': datetime.datetime.now().year,
        'query': query,       # Pass the query back to the template
        'no_results': no_results,
    })
  
def movie_id_view(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
        return render(request, 'movie_detail.html', {'movie_html': movie})
    except Movie.DoesNotExist:
        return HttpResponse("Movie not found", status=404)
    
def movie_details_view(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
        return render(request, f'movie_{pk}.html', {'movie': movie})
    except Movie.DoesNotExist:
        return HttpResponse("Movie not found", status=404)
    
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movie_detail.html', {'movie': movie})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponse("Registration successful")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            # Process the form data
            return HttpResponse("Profile updated successfully")
    else:
        form = ProfileForm()
    return render(request, 'profile.html', {'form': form})

def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            # Process the form data
            return HttpResponse("Profile updated successfully")
    else:
        form = ProfileForm()
    return render(request, 'profile_edit.html', {'form': form})

def profile_delete_view(request):
    if request.method == 'POST':
        # Here you would typically delete the user's profile
        return HttpResponse("Profile deleted successfully")
    return render(request, 'profile_delete.html')

@login_required

@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        return redirect('profile')
    return render(request, 'profile_edit.html', {'user': user})

def profile_delete_confirm_view(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')
    return render(request, 'profile_delete_confirm.html')

def movie_add(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie-list')
    else:
        form = MovieForm()
    return render(request, 'movie_form.html', {'form': form})

def CustomSignupView(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomSignupForm()
    return render(request, 'sign_up.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponse("Registration successful")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            # Process the form data
            return HttpResponse("Profile updated successfully")
    else:
        form = ProfileForm()
    return render(request, 'profile.html', {'form': form})

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            # Process the form data
            return HttpResponse("Profile updated successfully")
    else:
        form = ProfileForm()
    return render(request, 'profile_edit.html', {'form': form})

@login_required
def profile_delete_view(request):
    if request.method == 'POST':
        # Here you would typically delete the user's profile
        return HttpResponse("Profile deleted successfully")
    return render(request, 'profile_delete.html')

@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        return redirect('profile')
    return render(request, 'profile_edit.html', {'user': user})

def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie-list')
    else:
        form = MovieForm()
    return render(request, 'movie_form.html', {'form': form})

def cinema_prices_view(request, pk):
    """
    Shows prices for all cinemas AND upcoming showtimes for
    the movie specified by 'movie_id'.
    """
    
    # 1. Get the specific movie we want to see
    movie = get_object_or_404(Movie, pk=pk)
    
    # 2. Get the current time
    now = timezone.now()

    # 3. Create a Prefetch object to get ONLY upcoming showtimes for this movie.
    #    This is how we'll get the list of times for each cinema.
    showtimes_for_this_movie = Prefetch(
        'cinema_showtimes',
        # We filter for the movie AND for showtimes that are in the future
        queryset=Showtime.objects.filter(
            movie_id=movie.id,
            show_time__gte=now  # 'gte' means "greater than or equal to"
        ).order_by('show_time'),
        to_attr='filtered_showtimes' # The template will access this
    )

    # 4. Get ONLY the cinemas that have upcoming showtimes for this movie.
    #    This is the main fix. We no longer fetch cinemas that aren't playing the movie.
    relevant_cinemas = Cinema.objects.filter(
        cinema_showtimes__movie_id=movie.id,
        cinema_showtimes__show_time__gte=now
    ).distinct().prefetch_related(showtimes_for_this_movie)
    
    # 5. Get all other cinemas that DON'T have showtimes, just for price comparison
    other_cinemas = Cinema.objects.exclude(
        id__in=relevant_cinemas.values_list('id', flat=True)
    )

    context = {
        'cinemas_with_showtimes': relevant_cinemas, # Cinemas *with* showtimes
        'other_cinemas': other_cinemas,           # Cinemas *without* showtimes
        'movie': movie                            # The specific movie
    }
    return render(request, 'cinema_prices.html', context)
    
def cinema_prices_update_view(request, pk):
    """
    View to update cinema prices for a specific cinema.
    """
    cinema = get_object_or_404(Cinema, pk=pk)
    
    if request.method == 'POST':
        form = CinemaForm(request.POST, instance=cinema)
        if form.is_valid():
            form.save()
            return redirect('cinema_prices', pk=pk)  # Redirect to the cinema prices view
    else:
        form = CinemaForm(instance=cinema)
    
    return render(request, 'cinema_prices_update.html', {'form': form, 'cinema': cinema})


def cinema_prices_delete_view(request, pk):
    """
    View to delete a specific cinema.
    """
    cinema = get_object_or_404(Cinema, pk=pk)
    
    if request.method == 'POST':
        cinema.delete()
        return redirect('home')  # Redirect to home page after deletion
    
    return render(request, 'cinema_prices_delete.html', {'cinema': cinema})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Handle profile update logic here
        # Example: update user fields from request.POST
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        return redirect('profile')
    return render(request, 'profile_edit.html', {'user': user})

def CinemaUpdateView(UpdateView):
    model = Cinema
    form_class = CinemaForm
    template_name = 'cinema_update_form.html'
    success_url = reverse_lazy("home")

class CinemaUpdateView(UpdateView):
    model = Cinema
    form_class = CinemaForm
    template_name = 'cinema_update_form.html'
    success_url = reverse_lazy("home")