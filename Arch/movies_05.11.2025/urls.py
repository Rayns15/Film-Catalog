from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

# --- This file is now clean ---
# 1. No duplicate URL paths or names.
# 2. Only uses views that exist in your corrected 'views.py'.

urlpatterns = [
    # --- Admin ---
    path('admin/', admin.site.urls),

    # --- Main App & Movie Views ---
    # 'home_view' handles both the homepage and search results
    path('', views.afiseaza_home_page, name='home'),
    path('search/', views.afiseaza_home_page, name='movie_search'),

    # 'MovieDetailView' handles all movie detail pages
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),

    # CRUD (Create, Read, Update, Delete) for Movies
    path('movie/add/', views.MovieCreateView.as_view(), name='movie-add'),
    path('movie/<int:pk>/update/', views.MovieUpdateView.as_view(), name='movie-update'),
    path('movie/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie-delete'),

    # --- Cinema & Pricing Views ---
    path('movie/<int:movie_id>/prices/', views.cinema_prices_view, name='cinema_prices'), 
    path('prices/update/<int:pk>/', views.CinemaUpdateView.as_view(), name='cinema_prices_update'),
    # --- Auth Views (Login, Logout, Signup) ---
    path('login/', auth_views.LoginView.as_view(template_name='Log_in.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup_view, name='signup'),

    # --- Profile Views ---
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='profile_edit'),
    path('profile/delete/', views.profile_delete_view, name='profile_delete'),

    # --- Password Reset & Change ---
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

    # --- Static Pages & API ---
    path('aboutme/', TemplateView.as_view(template_name='aboutme.html'), name='aboutme'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('api/chat/', views.chat_api, name='chat_api'),

    # --- Old/Duplicate URLs (Removed) ---
    # All the conflicting paths for 'movie_details', 'movie/search', etc.
    # have been removed and replaced by the correct views above.
]