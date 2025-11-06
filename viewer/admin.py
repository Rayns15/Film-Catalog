from django.contrib import admin
from viewer.models import Movie
from viewer.models import Movie, Cinema, Showtime


# --- Showtime Inlines ---
# This creates a compact, table-like "inline" form.

class ShowtimeInlineForMovie(admin.TabularInline):
    """
    Lets you add/edit Showtimes from the Movie admin page.
    """
    model = Showtime
    # 'movie' is automatically set to the Movie you're editing
    fields = ('cinema', 'show_time') 
    extra = 1  # Shows one blank form for adding a new showtime
    autocomplete_fields = ['cinema'] # Makes cinema field a searchable dropdown

class ShowtimeInlineForCinema(admin.TabularInline):
    """
    Lets you add/edit Showtimes from the Cinema admin page.
    """
    model = Showtime
    # 'cinema' is automatically set to the Cinema you're editing
    fields = ('movie', 'show_time')
    extra = 1
    autocomplete_fields = ['movie'] # Makes movie field a searchable dropdown


# --- Main ModelAdmin Classes ---
# This is where we "attach" the inlines.

# in viewer/admin.py

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'year', 'genre_movie', 'rating')
    search_fields = ('title', 'director') # <-- Fixed
    list_filter = ('genre_movie', 'year')  # <-- Fixed
    inlines = [ShowtimeInlineForMovie]

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'Adult_ticket_price')
    search_fields = ('name', 'location') # Make Cinema searchable
    inlines = [ShowtimeInlineForCinema] # <-- ATTACHES THE INLINE

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    """
    (Optional) Registers a separate admin page for Showtimes.
    This is good for searching/filtering all showtimes at once.
    """
    list_display = ('movie', 'cinema', 'show_time')
    list_filter = ('cinema', 'movie', 'show_time')
    search_fields = ('movie__Title', 'cinema__name')
    autocomplete_fields = ['movie', 'cinema'] # Makes dropdowns searchable
# Register your models here.
