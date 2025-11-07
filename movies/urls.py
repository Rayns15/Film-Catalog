# În viewer/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from viewer import views  # Singurul import de view-uri de care aveți nevoie

# Importuri pentru fișierele media (pentru poze)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # === Pagina principală și Filme ===
    path('', views.afiseaza_home_page, name='home'),
    path('search/', views.movie_search_view, name='movie_search'),
    
    # === ACEASTA ESTE CALEA CORECTĂ ===
    # Trimite către Class-Based View (MovieDetailView), nu către o funcție veche
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    
    # CRUD Filme
    path('movie/add/', views.MovieCreateView.as_view(), name='movie-add'),
    path('movie/<int:pk>/update/', views.MovieUpdateView.as_view(), name='movie-update'),
    path('movie/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie-delete'),

    # === Prețuri Cinema și Showtimes ===
    path('movie/<int:pk>/prices/', views.cinema_prices_view, name='cinema_prices'),
    path('prices/update/<int:pk>/', views.CinemaUpdateView.as_view(), name='cinema_prices_update'),

    # === Autentificare ===
    path('login/', auth_views.LoginView.as_view(template_name='Log_in.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup_view, name='signup'),

    # === Profil ===
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='profile_edit'),
    path('profile/delete/', views.profile_delete_view, name='profile_delete'),

    # === Resetare Parolă ===
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

# --- Configurare Fișiere Media ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)