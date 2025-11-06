from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from viewer import views as viewer_views
from django.conf import settings
from django.conf.urls.static import static
from viewer.views import cinema_prices_update_view, movie_details_view, movie_id_view, movie_detail
from viewer.views import (
    MovieCreateView, MovieListView, MovieUpdateView, MovieDeleteView,
    base_view, inception_view, movie1_details, search, TheGodfatherView,
    movie_details_view, MovieDetailView, view_details, movie_details, movie_search, profile_view,
    profile_edit_view, profile_delete_view, profile_edit, movie_add, CustomSignupForm, cinema_prices_view, cinema_prices_update_view,)  # Ensure all necessary views are imported


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('home/', viewer_views.afiseaza_home_page, name='home_page'),
    path('create/', MovieCreateView.as_view(), name='movie_create'),
    path('list/', MovieListView.as_view(), name='movie-list'),
    path('update/<int:pk>/', MovieUpdateView.as_view(), name='movie-update'),
    path('delete/<int:pk>/', MovieDeleteView.as_view(), name='movie-delete'),
    path('base/', base_view, name='base'),  # Base view for the root URL
    path('inception/', inception_view, name='inception'),
    path('AddMovie/', MovieCreateView.as_view(), name='movie-add'),
    path('movie/<int:pk>/', movie_details_view, name='movie_details_view'),
    path('movie/<int:pk>/', movie_details_view, name='movie_id'),
    path('movie/<int:pk>/', movie_detail, name='movie-detail'),  # Detail view for a specific movie
    path('', viewer_views.afiseaza_home_page, name='home'),  # Root URL mapped to home_view
    path('movie_details/<int:pk>/', movie_details_view, name='movie_details'),
    path('login/', auth_views.LoginView.as_view(template_name='Log_in.html'), name='login'),
    path('signup/', viewer_views.signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('the_godfather/', TheGodfatherView.as_view(), name='the_godfather'),
    path('movie1/', MovieDetailView.as_view(), name='movie1'),
    path('movie1/<int:pk>/', movie1_details, name='movie1_details'),
    path('view/<int:pk>/', view_details.as_view(), name='view_details'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='Log_in.html'), name='account_login'),
    path('accounts/signup/', viewer_views.signup_view, name='account_signup'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='account_logout'),
    path('aboutme/', TemplateView.as_view(template_name='aboutme.html'), name='aboutme'),
    path('search/', search, name='movie_search'),  # Make sure your view matches this signature
    #path('search/', views.search, name='movie_search'),  # Make sure your view matches this signature
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('register/', viewer_views.signup_view, name='register'),
    path('profile/', profile_view, name='profile'),
    #path('profile/edit/', viewer_views.profile_edit_view, name='profile_edit'),  # Edit profile view
    path('profile/delete/', viewer_views.profile_delete_view, name='profile_delete'),  # Delete profile view
    path("profile/delete/confirm/", viewer_views.profile_delete_confirm_view, name="profile_delete_confirm"),
    path('profile/edit/', profile_edit, name='profile_edit'),  # Edit profile view
    path('movie/add/', movie_add, name='movie_add'),  # Add movie view
    path('movie/search/', movie_search, name='movie_search'),  # Movie search view
    path('movie/<int:pk>/', movie_details, name='movie_details'),  # Movie details view
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
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('CustomSignup/', viewer_views.CustomSignupView, name='custom_signup'),
    path('cinema_prices/<int:movie_id>/', viewer_views.cinema_prices_view, name='cinema_prices'),
    path('cinema-prices/<int:pk>/', viewer_views.cinema_prices_view, name='cinema_prices'),
    path('cinema-prices/<int:pk>/update/', viewer_views.cinema_prices_update_view, name='cinema_prices_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


