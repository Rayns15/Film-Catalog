
#!/bin/bash

# Recreate project urls to include the app urls
cat > "c:/Users/Rayns/OneDrive/Desktop/Python Curs/Django74/movies/urls.py" << 'PY'
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('viewer.urls')),
]
PY



# Fix viewer urls to use a relative import and only app-specific routes

cat > "c:/Users/Rayns/OneDrive/Desktop/Python Curs/Django74/viewer/urls.py" << 'PY'

from django.urls import path
from django.utils.module_loading import import_string


def lazy_view(dotted_path):
    def _wrapped(request, *args, **kwargs):
        view = import_string(dotted_path)
        return view(request, *args, **kwargs)
        from django.urls import path
        from django.utils.module_loading import import_string
        from django.views.generic import TemplateView
        from django.http import HttpResponse
        from django.shortcuts import render
        from django.views import View
        from django.views.generic import CreateView, ListView, UpdateView, DeleteView
        from django.urls import reverse_lazy
        from django.utils.functional import lazy
        from django.core.exceptions import ImproperlyConfigured
        from django.conf import settings
        from viewer.models import Movie
        from django import forms
        from django.db import models
        from django.db.models import Model, IntegerField, CharField
        from django.shortcuts import get_object_or_404
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        from django.views.decorators.csrf import csrf_exempt
        from viewer.views import afiseaza
        from viewer.views import MovieCreateView, MovieListView, MovieUpdateView, MovieDeleteView
        from viewer.views import shawshank_redemption_view, afiseaza_home_page
        from viewer.views import hello, search, phone_book, phone_book2, afiseaza, show_streams


def lazy_class_view(dotted_path):
    def _wrapped(request, *args, **kwargs):
        view_cls = import_string(dotted_path)
        return view_cls.as_view()(request, *args, **kwargs)
    return _wrapped


urlpatterns = [
    path('home/', lazy_view('viewer.views.afiseaza_home_page'), name='home'),
    path('create/', lazy_class_view('viewer.views.MovieCreateView'), name='movie-create'),
    path('list/', lazy_class_view('viewer.views.MovieListView'), name='movie-list'),
    path('shawshank-redemption/', lazy_view('viewer.views.shawshank_redemption_view'), name='shawshank-redemption'),
    path('update/<int:pk>/', lazy_class_view('viewer.views.MovieUpdateView'), name='movie-update'),
    path('delete/<int:pk>/', lazy_class_view('viewer.views.MovieDeleteView'), name='movie-delete'),
]
PY
echo "Script finished successfully."



# Fix settings to ensure the app is included and Django is setup

cat > "c:/Users/Rayns/OneDrive/Desktop/Python Curs/Django74/movies/settings.py" << 'PY'

from pathlib import Path



# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent



# Quick-start development settings - unsuitable for production

# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/



# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = 'django-insecure-placeholder'



# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True



ALLOWED_HOSTS = []



# Application definition



INSTALLED_APPS = [

    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',

    'viewer',

]



MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]



ROOT_URLCONF = 'movies.urls'



TEMPLATES = [

    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.debug',

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

            ],

        },

    },

]



WSGI_APPLICATION = 'movies.wsgi.application'



# Database

# https://docs.djangoproject.com/en/5.0/ref/settings/#databases



DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': BASE_DIR / 'db.sqlite3',

    }

}



# Password validation

# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators



AUTH_PASSWORD_VALIDATORS = [

    {

        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',

    },

    {

        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',

    },

    {

        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',

    },

    {

        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',

    },

]



# Internationalization

# https://docs.djangoproject.com/en/5.0/topics/i18n/



LANGUAGE_CODE = 'en-us'



TIME_ZONE = 'UTC'



USE_I18N = True



USE_TZ = True



# Static files (CSS, JavaScript, Images)

# https://docs.djangoproject.com/en/5.0/howto/static-files/



STATIC_URL = 'static/'



# Default primary key field type

# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PY



# After running the script to generate files, run Django commands separately

# For example, to run the development server:

# python "c:/Users/Rayns/OneDrive/Desktop/Python Curs/Django74/manage.py" runserver
# To make migrations and migrate the database:
# python "c:/Users/Rayns/OneDrive/Desktop/Python Curs/Django74/manage.py" makemigrations
# python "c:/Users/Rayns/OneDrive/Desktop/Python Curs/Django74/manage.py" migrate
# To create a superuser for admin access:
# python "c:/Users/Rayns/OneDrive/Desktop/Python Curs/Django74/manage.py" createsuperuser