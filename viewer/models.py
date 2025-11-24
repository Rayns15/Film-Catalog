from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    showtime = models.ForeignKey('Showtime', on_delete=models.CASCADE, related_name="bookings")
    # We will store seats as a comma-separated string, e.g., "A1,A2,B5"
    seats = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional: If you want to store the total cost calculated
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - {self.showtime} ({self.seats})"
    
    def get_seat_list(self):
        # Ensure seats is a string before splitting
        if not self.seats:
            return []
        return [seat.strip() for seat in str(self.seats).split(',')]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.user.username

class Movie(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    director = models.CharField(max_length=200, blank=True, null=True, db_column='director')
    year = models.IntegerField(blank=True, null=True, db_column='year')
    genre_movie = models.CharField(max_length=50, blank=True, null=True, db_column='genre_movie')
    cinema_price = models.IntegerField(blank=True, null=True, db_column='cinema_price')  # deprecated
    bio = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True, db_column='rating')
    profile_picture = models.ImageField(upload_to='movie_covers/', blank=True, null=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title or "Untitled Movie"

class ChatMessage(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="chat_messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message for {self.movie.title} by {self.user.username}"

class Cinema(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    Adult_ticket_price = models.IntegerField(blank=True, null=True)
    Child_ticket_price = models.IntegerField(blank=True, null=True)
    Senior_ticket_price = models.IntegerField(blank=True, null=True)
    Student_ticket_price = models.IntegerField(blank=True, null=True)

    weekend_surcharge = models.IntegerField(blank=True, null=True)
    holiday_surcharge = models.IntegerField(blank=True, null=True)
    weekday_discount = models.IntegerField(blank=True, null=True)
    matinee_discount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name or "Unnamed Cinema"

    def _get_weekend_price(self, base_price):
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
    
    def get_absolute_url(self):
        # Aici vom folosi 'cinema_detail' (numele URL-ului pe care-l vom crea)
        # cu primary key-ul cinematografului ca argument.
        return reverse('viewer:cinema_detail', kwargs={'pk': self.pk})

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showtimes")
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="cinema_showtimes")
    show_time = models.DateTimeField()

    def __str__(self):
        if self.movie and self.cinema and self.show_time:
            return f"{self.movie.title or 'Untitled'} at {self.cinema.name or 'Unknown Cinema'} ({self.show_time.strftime('%b %d, %I:%M %p')})"
        return "Invalid Showtime"

# class Comment(models.Model):
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"Comment by {self.user.username} on {self.movie.title}"