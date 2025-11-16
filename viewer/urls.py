# în viewer/urls.py (Fișierul NOU al Aplicației)

from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views  # <-- MODIFICARE IMPORTANTĂ: importă din folderul curent

# Nu ai nevoie de 'admin', 'include', 'settings' sau 'static' aici

urlpatterns = [
    # === Pagina principală și Filme ===
    # Am șters 'admin/' și 'include()' de aici
    path('api/chat/post/<int:movie_pk>/', views.post_chat_message, name='post-chat-message'),
    path('api/chat/delete/<int:message_pk>/', views.delete_chat_message, name='delete-chat-message'),
    path('showtime_create/', views.ShowtimeCreateView.as_view(), name='showtime_create'),

    #path('', views.afiseaza_home_page, name='home'),
    path('', views.movie_list, name='home'), # Am corectat name='home' aici
    
    # Am șters calea duplicată pentru 'search'
    path('search/', views.movie_search_view, name='movie_search'),

    # === ACEASTA ESTE CALEA CORECTĂ ===
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    
    # CRUD Filme
    path('movie/add/', views.MovieCreateView.as_view(), name='movie-add'),
    path('movie/<int:pk>/update/', views.MovieUpdateView.as_view(), name='movie-update'),
    path('movie/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie-delete'),

    # === Prețuri Cinema și Showtimes ===
    #path('movie/<int:pk>/prices/', views.CinemaPricesView.as_view(), name='cinema_prices'),
    # --- CORECTAT: Era 'as_IA_view()' ---
    path('prices/update/<int:pk>/', views.cinema_prices_update, name='cinema_prices_update'),
    path('movie/<int:pk>/prices/', views.cinema_prices.as_view(), name='cinema_prices'),
    path('cinemas/', views.cinema_list_view, name='cinema-list'),
    path('showtimes/add/', views.add_showtime_view, name='add-showtime'),
    path('cinemas/add/', views.cinema_add_view, name='cinema-add'),
    path('schedule/new/', views.ShowtimeCreateView.as_view(), name='showtime_create'),
    path('schedule/<int:pk>/update/', views.ShowtimeUpdateView.as_view(), name='showtime_update'),
    path('schedule/<int:pk>/delete/', views.ShowtimeDeleteView.as_view(), name='showtime_delete'),

    # === Autentificare ===
    path('login/', auth_views.LoginView.as_view(template_name='Log_in.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup_view, name='signup'),

    # === Profil ===
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/<int:pk>/', views.edit_profile, name='profile_edit'),
    path('profile/delete/', views.profile_delete_view, name='profile_delete'),

    # === Resetare Parolă (totul este corect) ===
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_change/', 
         auth_views.PasswordChangeView.as_view(template_name='password_change.html'), 
         name='password_change'),
    path('password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), 
         name='password_change_done'),

    # === Pagini Statice & API ===
    path('aboutme/', TemplateView.as_view(template_name='aboutme.html'), name='aboutme'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('api/chat/', views.chat_api, name='chat_api'),
]