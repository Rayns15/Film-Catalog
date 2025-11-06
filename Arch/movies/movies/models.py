from django.db import models
from django.db.models import Model, IntegerField, CharField
from django import forms
from django.contrib.auth.models import User

class Cinema(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    
    # Base prices
    Adult_ticket_price = models.IntegerField(blank=True, null=True) # Assuming IntegerField, change to DecimalField if needed
    Child_ticket_price = models.IntegerField(blank=True, null=True)
    Senior_ticket_price = models.IntegerField(blank=True, null=True)
    Student_ticket_price = models.IntegerField(blank=True, null=True)
    
    # Surcharges
    weekend_surcharge = models.IntegerField(blank=True, null=True)
    # ... other fields ...

    class Meta:
        app_label = 'movies'

    def __str__(self):
        return self.name

    # --- ADD THESE PROPERTIES ---

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

class Movie(Model):
    Title = CharField(max_length=100, blank=True, null=True, db_column='title')
    director = CharField(max_length=100, blank=True, null=True, db_column='director')
    Year = IntegerField(blank=True, null=True, db_column='year')
    genre_movie = CharField(max_length=50, blank=True, null=True, db_column='genre_movie')
    rating = IntegerField(blank=True, null=True, db_column='rating')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='movie_covers/', blank=True, null=True)

    class Meta:
        app_label = 'movies'

class Showtime(models.Model):
    """
    This is the "bridge" model that connects a Movie to a Cinema.
    """
    # Foreign Key to Movie: One movie can have many showtimes
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showtimes")
    
    # Foreign Key to Cinema: One cinema can have many showtimes
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="cinema_showtimes")
    
    # The specific date and time of this showing
    show_time = models.DateTimeField()
    
    # You could even add a specific price FOR THIS SHOWING (e.g., for 3D)
    # price_multiplier = models.DecimalField(default=1.0, max_digits=3, decimal_places=1)

    # --- ADDED META CLASS ---
    class Meta:
        app_label = 'movies'


class Profile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = CharField(max_length=15, blank=True, null=True, db_column='telefon')
    email = CharField(max_length=100, blank=True, null=True, db_column='email')
    
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    class Meta:
        app_label = 'movies'

    # --- CLEANED UP __str__ METHOD ---
    def __str__(self):
        return self.user.username