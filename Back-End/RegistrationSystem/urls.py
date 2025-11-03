# RegistrationSystem/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # ربط مسارات تطبيق academic تحت /api/
    path('api/', include('academic.urls')), 
]