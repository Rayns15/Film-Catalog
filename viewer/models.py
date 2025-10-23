from django.db import models
from django.db.models import Model, IntegerField, CharField
from django import forms
from django.contrib.auth.models import User

# Create your models here.

class Movie(Model):
    Title = CharField(max_length=100, blank=True, null=True, db_column='title')
    director = CharField(max_length=100, blank=True, null=True, db_column='director')
    Year = IntegerField(blank=True, null=True, db_column='year')
    cinema_price = IntegerField(blank=True, null=True, db_column='cinema_price')
    genre_movie = CharField(max_length=50, blank=True, null=True, db_column='genre_movie')
    
    
class Profile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = CharField(max_length=15, blank=True, null=True, db_column='telefon')
    email = CharField(max_length=100, blank=True, null=True, db_column='email')



    

    


