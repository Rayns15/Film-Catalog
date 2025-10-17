from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from viewer import views as viewer_views
# This file is intentionally left blank.
from viewer.views import *  # Ensure views are imported if views.py exists
from viewer.views import (
    MovieCreateView, MovieListView, MovieUpdateView, MovieDeleteView,
    base_view, inception_view, movie1_details, search, TheGodfatherView, 
    movie_details_view, MovieDetailView)  # Ensure all necessary views are imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', viewer_views.afiseaza_home_page, name='home_page'),
    path('create/', MovieCreateView.as_view(), name='movie-create'),
    path('list/', MovieListView.as_view(), name='movie-list'),
    path('update/<int:pk>/', MovieUpdateView.as_view(), name='movie-update'),
    path('delete/<int:pk>/', MovieDeleteView.as_view(), name='movie-delete'),
    path('base/', base_view, name='base'),  # Base view for the root URL
    path('inception/', inception_view, name='inception'),
    path('AddMovie/', MovieCreateView.as_view(), name='add_movie'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),  # Detail view for a specific movie
    path('', viewer_views.afiseaza_home_page, name='home'),  # Root URL mapped to home_view
    path('movie_details/<int:id>/', movie_details_view, name='movie_details'),
    path('login/', auth_views.LoginView.as_view(template_name='Log_in.html'), name='login'),
    path('signup/', viewer_views.signup, name='signup'),
]




