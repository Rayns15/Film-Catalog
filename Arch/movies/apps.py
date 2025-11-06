from django.apps import AppConfig


class MoviesConfig(AppConfig):  # <-- Rename the class
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies' # <-- THIS IS THE FIX
