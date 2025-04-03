from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('vet_supplies/', include('vet_supplies.urls')),
    path('office_supplies/', include('office_supplies.urls')),
    path('reports/', include('reports.urls')),
]