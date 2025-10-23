from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from viewer import views as viewer_views
from viewer.views import movie_details_view, movie_id_view, movie_detail
from viewer.views import (
    MovieCreateView, MovieListView, MovieUpdateView, MovieDeleteView,
    base_view, inception_view, movie1_details, search, TheGodfatherView,
    movie_details_view, MovieDetailView, view_details, movie_details, movie_search, profile_view, 
    profile_edit_view, profile_delete_view, profile_edit, movie_add)  # Ensure all necessary views are imported
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('home/', viewer_views.afiseaza_home_page, name='home_page'),
    path('create/', MovieCreateView.as_view(), name='movie-create'),
    path('list/', MovieListView.as_view(), name='movie-list'),
    path('update/<int:pk>/', MovieUpdateView.as_view(), name='movie-update'),
    path('delete/<int:pk>/', MovieDeleteView.as_view(), name='movie-delete'),
    path('base/', base_view, name='base'),  # Base view for the root URL
    path('inception/', inception_view, name='inception'),
    path('AddMovie/', MovieCreateView.as_view(), name='add_movie'),
    path('movie/<int:pk>/', movie_details_view, name='movie_details_view'),
    path('movie/<int:pk>/', movie_details_view, name='movie_id'),
    path('movie/<int:pk>/', movie_detail, name='movie_detail'),  # Detail view for a specific movie
    path('', viewer_views.afiseaza_home_page, name='home'),  # Root URL mapped to home_view
    path('movie_details/<int:pk>/', movie_details_view, name='movie_details'),
    path('login/', auth_views.LoginView.as_view(template_name='Log_in.html'), name='login'),
    path('signup/', viewer_views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('the_godfather/', TheGodfatherView.as_view(), name='the_godfather'),
    path('movie1/', MovieDetailView.as_view(), name='movie1'),
    path('movie1/<int:pk>/', movie1_details, name='movie1_details'),
    path('view/<int:pk>/', view_details.as_view(), name='view_details'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='Log_in.html'), name='account_login'),
    path('accounts/signup/', viewer_views.signup, name='account_signup'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='account_logout'),
    path('aboutme/', TemplateView.as_view(template_name='aboutme.html'), name='aboutme'),
    path('search/', search, name='movie_search'),  # Make sure your view matches this signature
    #path('search/', views.search, name='movie_search'),  # Make sure your view matches this signature
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('register/', viewer_views.register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    #path('profile/edit/', viewer_views.profile_edit_view, name='profile_edit'),  # Edit profile view
    path('profile/delete/', viewer_views.profile_delete_view, name='profile_delete'),  # Delete profile view
    path("profile/delete/confirm/", viewer_views.profile_delete_confirm_view, name="profile_delete_confirm"),
    path('profile/edit/', profile_edit, name='profile_edit'),  # Edit profile view
    path('movie/add/', movie_add, name='movie_add'),  # Add movie view
]




