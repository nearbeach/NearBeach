from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v0/', include('NearBeach.urls_api_v0')),
    path('', include('NearBeach.urls')),
]