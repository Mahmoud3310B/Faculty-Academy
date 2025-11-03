
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView 
from django.conf import settings   
from django.conf.urls.static import static 
from academic.views import management_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('academic.urls')),
    path('', TemplateView.as_view(template_name='login.html'), name='home'),
    path('login.html', TemplateView.as_view(template_name='login.html'), name='login_page'), 
    path('management.html', TemplateView.as_view(template_name='management.html'), name='management_page'), 
    path('index.html', TemplateView.as_view(template_name='index.html'), name='index_page'), 
    path('catalog.html', TemplateView.as_view(template_name='catalog.html'), name='catalog_page'),
    path('payment.html', TemplateView.as_view(template_name='payment.html'), name='payment_page'),
    path('profile.html', TemplateView.as_view(template_name='profile.html'), name='profile_page'),
    path('schedule.html', TemplateView.as_view(template_name='schedule.html'), name='schedule_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])