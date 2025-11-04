from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView 
from django.conf import settings   
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('academic.urls')),
    path('login', TemplateView.as_view(template_name='login.html'), name='login_page'), 
    path('management', TemplateView.as_view(template_name='management.html'), name='management_page'), 
    path('index', TemplateView.as_view(template_name='index.html'), name='index_page'), 
    path('catalog', TemplateView.as_view(template_name='catalog.html'), name='catalog_page'),
    path('payment', TemplateView.as_view(template_name='payment.html'), name='payment_page'),
    path('profile', TemplateView.as_view(template_name='profile.html'), name='profile_page'),
    path('schedule', TemplateView.as_view(template_name='schedule.html'), name='schedule_page'),
]
