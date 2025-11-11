from django.contrib import admin
from viewer.models import Movie, Cinema, Showtime, ChatMessage, Profile


# --- Showtime Inlines ---
# This creates a compact, table-like "inline" form.

class ProfileInline(admin.StackedInline):
    """
    Lets you edit Profile info directly on the User admin page.
    """
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'  # Explicitly specify the foreign key field

class ChatMessageInline(admin.TabularInline):
    """
    Lets you view/add/delete ChatMessages directly from the Movie admin page.
    """
    model = ChatMessage
    fields = ('user', 'message', 'timestamp')
    readonly_fields = ('timestamp',)
    extra = 1
    autocomplete_fields = ['user'] # Makes user field a searchable dropdown

class ShowtimeInlineForMovie(admin.TabularInline):
    model = Showtime
    fields = ('cinema', 'show_time')
    extra = 1
    autocomplete_fields = ['cinema'] # Makes cinema field a searchable dropdown

class ShowtimeInlineForCinema(admin.TabularInline):
    model = Showtime
    fields = ('movie', 'show_time')
    extra = 1
    autocomplete_fields = ['movie'] # Makes movie field a searchable dropdown


# --- Main ModelAdmin Classes ---
# This is where we "attach" the inlines.

# in viewer/admin.py

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'year', 'genre_movie', 'rating')
    search_fields = ('title', 'director')
    list_filter = ('genre_movie', 'year')
    # --- 3. Add ChatMessageInline to this list ---
    inlines = [ShowtimeInlineForMovie, ChatMessageInline]

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'Adult_ticket_price')
    search_fields = ('name', 'location')
    inlines = [ShowtimeInlineForCinema]

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'message', 'timestamp')
    list_filter = ('movie', 'user')
    search_fields = ('message', 'user__username', 'movie__title')

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
