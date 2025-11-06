from django.db import models
from django.db.models import Model, IntegerField, CharField
from django import forms
from django.contrib.auth.models import User

# Create your models here.

from django.db import models
from django.db.models import Model, IntegerField, CharField, TextField

class Movie(models.Model):
    name = models.CharField(max_length=200)
    
    @property
    def title(self):
        return self.name
# === The Movie Model (Corrected) ===
# Note: I removed 'cinema_price' from this model.
# Price is a property of the Cinema, not the Movie.
# in viewer/models.py

class Movie(Model):
    # --- FIXED: Changed 'Title' to 'title' ---
    title = CharField(max_length=100, blank=True, null=True, db_column='title')
    
    director = CharField(max_length=100, blank=True, null=True, db_column='director')
    
    # --- FIXED: Changed 'Year' to 'year' ---
    year = IntegerField(blank=True, null=True, db_column='year')
    
    genre_movie = CharField(max_length=50, blank=True, null=True, db_column='genre_movie')
    
    # Deprecated: kept for backward compatibility
    cinema_price = IntegerField(blank=True, null=True, db_column='cinema_price')
    
    # Other fields
    bio = TextField(blank=True, null=True)
    rating = IntegerField(blank=True, null=True, db_column='rating')
    profile_picture = models.ImageField(upload_to='movie_covers/', blank=True, null=True)

    def __str__(self):
        # --- FIXED: Use self.title (lowercase) ---
        return self.title or "Untitled Movie"

# === The New Cinema Model ===
# This model holds information about the theater location and its base prices.
class Cinema(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # --- Price logic lives here ---
    # (Using IntegerField to match your style, but models.DecimalField is
    #  highly recommended for working with money.)
    
    # Base prices
    Adult_ticket_price = models.IntegerField(blank=True, null=True)
    Child_ticket_price = models.IntegerField(blank=True, null=True)
    Senior_ticket_price = models.IntegerField(blank=True, null=True)
    Student_ticket_price = models.IntegerField(blank=True, null=True)
    
    # Surcharges/Discounts
    weekend_surcharge = models.IntegerField(blank=True, null=True)
    holiday_surcharge = models.IntegerField(blank=True, null=True)
    weekday_discount = models.IntegerField(blank=True, null=True)
    matinee_discount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name or "Unnamed Cinema"

    # --- Properties to safely calculate prices ---
    # (These are from your previous models.py file and are a great idea)
    
    def _get_weekend_price(self, base_price):
        """Helper function to safely add price and surcharge."""
        price = base_price or 0
        surcharge = self.weekend_surcharge or 0
        return price + surcharge

    @property
    def adult_weekend_price(self):
        return self._get_weekend_price(self.Adult_ticket_price)

    @property
    def child_weekend_price(self):
        return self._get_weekend_price(self.Child_ticket_price)

    @property
    def senior_weekend_price(self):
        return self._get_weekend_price(self.Senior_ticket_price)

    @property
    def student_weekend_price(self):
        return self._get_weekend_price(self.Student_ticket_price)


# === The New Showtime "Bridge" Model ===
# This model connects one Movie to one Cinema at a specific time.
class Showtime(models.Model):
    # Foreign Key to Movie: One movie can have many showtimes
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showtimes")
    
    # Foreign Key to Cinema: One cinema can have many showtimes
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="cinema_showtimes")
    
    # The specific date and time of this showing
    show_time = models.DateTimeField()

    def __str__(self):
        try:
            return f"{self.movie.Title} at {self.cinema.name} ({self.show_time.strftime('%b %d, %I:%M %p')})"
        except:
            return "Invalid Showtime"    
    
class Profile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = CharField(max_length=15, blank=True, null=True, db_column='telefon')
    email = CharField(max_length=100, blank=True, null=True, db_column='email')



    

    


