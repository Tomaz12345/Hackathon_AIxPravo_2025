from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.urls import path, include

def home(request):
    return HttpResponse("Welcome to the Brand Checker API")

urlpatterns = [
    path("", home),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    #path('api/', include('scraper.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve media files in development
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)