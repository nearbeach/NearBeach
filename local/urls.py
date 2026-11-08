from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('silk/', include('silk.urls', namespace='silk')),
    path('admin/', admin.site.urls),
    path('o/', include('NearBeach.urls.oauth2')),
    path('', include('NearBeach.urls.base')),
]