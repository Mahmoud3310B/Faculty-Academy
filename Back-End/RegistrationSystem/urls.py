# Back-End/RegistrationSystem/urls.py (الكامل والمُحدث)

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView 
from django.conf import settings # لاستخدام إعدادات static
from django.conf.urls.static import static # لخدمة الملفات الثابتة في بيئة التطوير
from academic.views import management_view

urlpatterns = [
    # 1. مسار الإدارة والـ API
    path('admin/', admin.site.urls),
    path('api/', include('academic.urls')),
    
    # ===============================================
    # 2. مسارات خدمة ملفات الواجهة الأمامية (Frontend HTML)
    # ===============================================

    # الصفحات الرئيسية (login, management, index)
    path('', TemplateView.as_view(template_name='login.html'), name='home'),
    path('login.html', TemplateView.as_view(template_name='login.html'), name='login_page'), 
    path('management.html', TemplateView.as_view(template_name='management.html'), name='management_page'), 
    path('index.html', TemplateView.as_view(template_name='index.html'), name='index_page'), 
    
    # الصفحات الأخرى
    path('catalog.html', TemplateView.as_view(template_name='catalog.html'), name='catalog_page'),
    path('payment.html', TemplateView.as_view(template_name='payment.html'), name='payment_page'),
    path('profile.html', TemplateView.as_view(template_name='profile.html'), name='profile_page'),
    path('schedule.html', TemplateView.as_view(template_name='schedule.html'), name='schedule_page'),
]

# 3. خدمة الملفات الثابتة (Static Files) في بيئة التطوير
# هذا ضروري لكي يتم تحميل CSS/JS/Images في Debug=True
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])