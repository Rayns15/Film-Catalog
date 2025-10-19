from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from viewer.models import Movie
from django.db.models import Model, IntegerField, CharField
from django.views import View
from django.shortcuts import render
from django import forms
# Create your views here.

def base_view(request):
    return render(request, 'base.html')

def search(request):
    query = request.GET.get('q', '')
    movies = Movie.objects.filter(Title__icontains=query)
    return render(request, 'home.html', {'movies_html': movies})
    
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
_BASE_FIELDS = ['Title', 'director', 'Year', 'cinema_price']
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
    context_object_name = 'movie_html'
    template_name = 'movie_detail.html'  # Default template

    def get_template_names(self):
        if self.object:
            return [f'movie_{self.object.id}.html', self.template_name]
        return [self.template_name]

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
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Here you would typically create the user
            return HttpResponse(f"User {username} signed up successfully")
    else:
        form = SignupForm()
    return render(request, 'Sign_up.html', {'form': form})

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
    return render(request, 'Sign_up.html', {'form': form})

def movie_search(request):
    query = request.GET.get('q', '')
    movies = Movie.objects.filter(Title__icontains=query)
    streams = Stream.objects.all()
    return render(request, 'home.html', {
        'movies_html': movies,
        'streams_html': streams,
        'user': request.user,
        'year': datetime.datetime.now().year,
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
    try:
        movie = Movie.objects.get(pk=pk)
        return render(request, 'movie_detail.html', {'movie': movie})
    except Movie.DoesNotExist:
        return HttpResponse("Movie not found", status=404)
    
