# viewer/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views
from viewer.views import movie_list

app_name = 'viewer' 

urlpatterns = [
    # === Pagina principală și Filme ===
    # O SINGURĂ intrare pentru 'home', care folosește movie_list
    path('', movie_list, name='home'), 
    path('search/', views.movie_search_view, name='movie_search'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    
    # CRUD Filme (Doar pentru staff/admin)
    path('movie/add/', views.MovieCreateView.as_view(), name='movie-add'),
    #path('movie/create/', views.MovieCreateView.as_view(), name='movie-create'),
    path('movie/<int:pk>/update/', views.MovieUpdateView.as_view(), name='movie-update'),
    path('movie/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie-delete'),

    # === Cinematografe și Prețuri ===
    path('cinemas/', views.CinemaListView.as_view(), name='cinema-list'),
    path('cinemas/<int:pk>/', views.CinemaDetailView.as_view(), name='cinema_detail'),
    path('cinemas/add/', views.cinema_add_view, name='cinema-add'), # Pentru staff
    path('movie/<int:pk>/prices/', views.cinema_prices.as_view(), name='cinema_prices'),
    path('prices/update/<int:pk>/', views.cinema_prices_update, name='cinema_prices_update'), # Pentru staff

    # === Showtimes ===
    path('schedule/new/', views.ShowtimeCreateView.as_view(), name='showtime_create'),
    path('schedule/<int:pk>/update/', views.ShowtimeUpdateView.as_view(), name='showtime_update'),
    path('schedule/<int:pk>/delete/', views.ShowtimeDeleteView.as_view(), name='showtime_delete'),
    path('schedule/', views.ShowtimeListView.as_view(), name='showtime_list'),
    path('schedule/<int:pk>/', views.ShowtimeDetailView.as_view(), name='showtime_detail'),
    # === Chat API ===
    path('api/chat/post/<int:movie_pk>/', views.post_chat_message, name='post-chat-message'),
    path('api/chat/delete/<int:message_pk>/', views.delete_chat_message, name='delete-chat-message'),
    path('api/chat/', views.chat_api, name='chat_api'),

    # === Autentificare & Profil ===
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='Log_in.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Redirect corect spre 'home' fara namespace
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/<int:pk>/', views.edit_profile, name='profile_edit'),
    path('profile/delete/', views.profile_delete_view, name='profile_delete'),

    # === Resetare Parolă ===
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

    # === Pagini Statice ===
    path('aboutme/', TemplateView.as_view(template_name='aboutme.html'), name='aboutme'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
]