# în movies/urls.py (Fișierul Proiectului)

from django.contrib import admin
from django.urls import path, include  # Asigură-te că 'include' este importat
from django.conf import settings
from django.conf.urls.static import static

# NU mai importa 'views', 'auth_views', sau 'TemplateView' aici

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Această linie este acum corectă și va încărca fișierul de mai jos
    path('', include('viewer.urls')), 
     
]

# Păstrează configurarea pentru fișierele media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)