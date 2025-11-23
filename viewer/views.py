# viewer/views.py

from django.core.paginator import Paginator
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
from .forms import (
    ShowtimeForm, CinemaForm, MovieForm, ProfileForm,
    CustomSignupForm, RegisterForm # Asigurați-vă că acestea există în forms.py
)
from django.template.defaultfilters import register as default_template_register

# === Filtru Template ===
@default_template_register.filter(name='add_class')
def add_class(field, css_classes):
    try:
        existing = field.field.widget.attrs.get('class', '')
        combined = f"{existing} {css_classes}".strip()
        return field.as_widget(attrs={**field.field.widget.attrs, 'class': combined})
    except Exception:
        return field

# === Vederi principale (Filme, Cinematografe) ===

def movie_list(request):
    """ Pagina principală (HOME) - afișează lista de filme și gestionează căutarea. """
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
    """ Pagină dedicată pentru rezultatele căutării. """
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

class CinemaListView(ListView):
    """ Afișează lista de carduri pentru cinematografe. """
    model = Cinema
    template_name = 'cinemas/cinema_list.html'
    context_object_name = 'cinemas'
    queryset = Cinema.objects.all().order_by('name')

class CinemaDetailView(DetailView):
    """ Afișează detaliile unui singur cinematograf și showtimes-urile sale. """
    model = Cinema
    template_name = 'cinemas/cinema_detail.html'
    context_object_name = 'cinema'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['showtimes'] = Showtime.objects.filter(cinema=self.object).order_by('show_time', 'movie__title')
        return context

# === CRUD Filme (Class-Based Views) ===

class MovieCreateView(CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movie_form.html'
    success_url = reverse_lazy("viewer:home") # Corectat să folosească app_name

class MovieUpdateView(UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movie_update.html'
    success_url = reverse_lazy("viewer:home") # Corectat să folosească app_name

class MovieDeleteView(DeleteView):
    model = Movie
    template_name = 'movie_confirm_delete.html'
    success_url = reverse_lazy("viewer:home") # Corectat să folosească app_name

class MovieDetailView(DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'movie_detail.html'

# === CRUD Showtimes (Class-Based Views) ===

class ShowtimeListView(ListView):
    """ Afișează lista de showtimes cu paginare, filtrare și sortare. """
    model = Showtime
    template_name = 'showtime_list.html'
    context_object_name = 'showtimes'
    paginate_by = 5

    def get_queryset(self):
        showtime_list = Showtime.objects.select_related('movie', 'cinema')
        
        # Filtrare
        movie_filter = self.request.GET.get('movie_filter', None)
        cinema_filter = self.request.GET.get('cinema_filter', None)
        date_filter = self.request.GET.get('date_filter', None)
        if movie_filter:
            showtime_list = showtime_list.filter(movie__title__icontains=movie_filter)
        if cinema_filter:
            showtime_list = showtime_list.filter(cinema__name__icontains=cinema_filter)
        if date_filter:
            showtime_list = showtime_list.filter(show_time__date=date_filter)

        # Sortare
        sort_by = self.request.GET.get('sort', '-show_time')
        valid_sort_fields = [
            'movie__title', '-movie__title', 'cinema__name', 
            '-cinema__name', 'show_time', '-show_time'
        ]
        if sort_by not in valid_sort_fields:
            sort_by = '-show_time'
        showtime_list = showtime_list.order_by(sort_by)

        return showtime_list

class ShowtimeDetailView(DetailView):
    """ Afișează detaliile unui showtime specific. """
    model = Showtime
    template_name = 'cinemas/add_showtime.html'
    context_object_name = 'showtime'

class ShowtimeCreateView(CreateView):
    """ Pagina 'Showtime Manager' - creează și listează showtimes. """
    model = Showtime
    form_class = ShowtimeForm
    template_name = 'add_showtime.html'
    success_url = reverse_lazy('viewer:showtime_create') # Corectat

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        showtime_list = Showtime.objects.select_related('movie', 'cinema')
        
        # Filtrare
        movie_filter = self.request.GET.get('movie_filter', None)
        cinema_filter = self.request.GET.get('cinema_filter', None)
        date_filter = self.request.GET.get('date_filter', None)
        if movie_filter:
            showtime_list = showtime_list.filter(movie__title__icontains=movie_filter)
        if cinema_filter:
            showtime_list = showtime_list.filter(cinema__name__icontains=cinema_filter)
        if date_filter:
            showtime_list = showtime_list.filter(show_time__date=date_filter)

        # Sortare
        sort_by = self.request.GET.get('sort', '-show_time')
        valid_sort_fields = [
            'movie__title', '-movie__title', 'cinema__name', 
            '-cinema__name', 'show_time', '-show_time'
        ]
        if sort_by not in valid_sort_fields:
            sort_by = '-show_time'
        showtime_list = showtime_list.order_by(sort_by)

        # Paginare
        paginator = Paginator(showtime_list, 5) # 5 elemente pe pagină
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        context['page_obj'] = page_obj
        context['current_sort'] = sort_by
        return context

class ShowtimeUpdateView(UpdateView):
    """ Pagina de update pentru un showtime, refolosește același template. """
    model = Showtime
    form_class = ShowtimeForm
    template_name = 'add_showtime.html'
    success_url = reverse_lazy('viewer:showtime_create') # Corectat

    def get_context_data(self, **kwargs):
        # Logica este identică cu cea de la CreateView
        context = super().get_context_data(**kwargs)
        showtime_list = Showtime.objects.select_related('movie', 'cinema')
        
        # Filtrare
        movie_filter = self.request.GET.get('movie_filter', None)
        cinema_filter = self.request.GET.get('cinema_filter', None)
        date_filter = self.request.GET.get('date_filter', None)
        if movie_filter:
            showtime_list = showtime_list.filter(movie__title__icontains=movie_filter)
        if cinema_filter:
            showtime_list = showtime_list.filter(cinema__name__icontains=cinema_filter)
        if date_filter:
            showtime_list = showtime_list.filter(show_time__date=date_filter)

        # Sortare
        sort_by = self.request.GET.get('sort', '-show_time')
        valid_sort_fields = [
            'movie__title', '-movie__title', 'cinema__name', 
            '-cinema__name', 'show_time', '-show_time'
        ]
        if sort_by not in valid_sort_fields:
            sort_by = '-show_time'
        showtime_list = showtime_list.order_by(sort_by)

        # Paginare
        paginator = Paginator(showtime_list, 5) # 5 elemente pe pagină
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        context['page_obj'] = page_obj
        context['current_sort'] = sort_by
        return context

class ShowtimeDeleteView(DeleteView):
    model = Showtime
    template_name = 'showtime_confirm_delete.html' 
    success_url = reverse_lazy('viewer:showtime_create') # Corectat

# === Vederi pentru Staff (Funcții) ===

@staff_member_required
def cinema_add_view(request):
    """ Formular pentru adăugarea unui cinematograf nou. """
    if request.method == 'POST':
        form = CinemaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cinema '{form.cleaned_data['name']}' added successfully!")
            return redirect('viewer:cinema-list') # Corectat
    else:
        form = CinemaForm()
    return render(request, 'cinema_form.html', {'form': form})

@staff_member_required
def cinema_prices_update(request, pk):
    """ Formular pentru actualizarea prețurilor unui cinematograf. """
    cinema = get_object_or_404(Cinema, pk=pk)
    next_url = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'POST':
        form = CinemaForm(request.POST, instance=cinema)
        if form.is_valid():
            form.save()
            messages.success(request, f"Prices for '{cinema.name}' updated successfully!")
            return redirect(next_url or 'viewer:cinema-list') # Corectat
    else:
        form = CinemaForm(instance=cinema)

    context = {'form': form, 'cinema': cinema, 'next_url': next_url}
    return render(request, 'cinema_prices_update.html', context)

class cinema_prices(DetailView):
    """ Afișează prețurile și showtimes-urile unui film, grupate pe cinematograf. """
    model = Movie
    template_name = 'cinema_prices.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        now = timezone.now()
        
        # Optimizare: Preia showtimes-urile relevante pentru acest film
        showtimes_for_this_movie = Prefetch(
            'cinema_showtimes',
            queryset=Showtime.objects.filter(
                movie_id=movie.pk,
                show_time__gte=now # Arată doar showtimes viitoare
            ).order_by('show_time'),
            to_attr='filtered_showtimes'
        )
        
        # Preia cinematografele care au showtimes viitoare pentru acest film
        cinemas_with_showtimes = Cinema.objects.filter(
            cinema_showtimes__movie_id=movie.pk,
            cinema_showtimes__show_time__gte=now
        ).distinct().prefetch_related(showtimes_for_this_movie)
        
        context['cinemas_with_showtimes'] = cinemas_with_showtimes
        context['chat_messages'] = ChatMessage.objects.filter(movie=movie)
        return context

# === API pentru Chat ===

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
            movie=movie, user=request.user, message=message_text
        )
        return JsonResponse({
            'status': 'ok',
            'message': chat_message.message,
            'user': chat_message.user.username,
            'timestamp': chat_message.timestamp.strftime('%b %d, %I:%M %p'),
            'message_id': chat_message.pk
        })
    except Movie.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Movie not found'}, status=44)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

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

def chat_api(request):
    return HttpResponse("Chat API is working!")

# === Autentificare & Profil (Funcții) ===

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST) # Folosind CustomSignupForm
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User {user.username} signed up successfully!")
            return redirect('viewer:login') # Corectat
    else:
        form = CustomSignupForm()
    return render(request, 'sign_up.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST) 
        if form.is_valid():
            return HttpResponse("Profile updated successfully")
    else:
        form = ProfileForm()
    return render(request, 'profile.html', {'form': form})

@login_required
def edit_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user != user:
        return redirect('viewer:home') # Corectat
        
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        return redirect('viewer:profile') # Corectat
    return render(request, 'profile_edit.html', {'user': user})

@login_required
def profile_delete_view(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Profile deleted successfully")
        return redirect('viewer:home') # Corectat
    return render(request, 'profile_delete.html')