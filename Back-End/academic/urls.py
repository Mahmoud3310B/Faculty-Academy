# academic/urls.py (الكود الكامل والمدمج)

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView 
from .views import (
    LoginView, 
    CourseListView, 
    RegisterCourseView, 
    CancelRegistrationView, # ✅ تم استيراد View الجديدة
    StudentScheduleView,
    # Payments
    InitiatePaymentView,
    PaymentUpdateView,
    PaymentHistoryView,
    # Admin & Instructor
    AdminCourseCreateView, 
    AdminInstructorCreateView, # ✅ تم استيراد View الجديدة
    AdminStudentListView,
    AdminStudentDetailView,
    InstructorGradeUpdateView,
    # Views الأخرى
    AdminCourseListView, 
    InstructorCoursesListView, 
    CourseRegisteredStudentsView, 
    NotificationCreateView, 
    NotificationListView, 
)

urlpatterns = [
    # ====================================================
    # 1. المصادقة (Authentication)
    # ====================================================
    path('token/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ====================================================
    # 2. وظائف الطالب (Student)
    # ====================================================
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('register/', RegisterCourseView.as_view(), name='course-register'),
    path('cancel-registration/', CancelRegistrationView.as_view(), name='course-cancel'), # ✅ المسار الجديد لإلغاء التسجيل
    path('schedule/', StudentScheduleView.as_view(), name='student-schedule'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),

    # ====================================================
    # 3. المدفوعات (Payments)
    # ====================================================
    path('payments/initiate/', InitiatePaymentView.as_view(), name='payment-initiate'),
    path('payments/update/', PaymentUpdateView.as_view(), name='payment-update'),
    path('payments/history/', PaymentHistoryView.as_view(), name='payment-history'),

    # ====================================================
    # 4. وظائف المسؤول (Admin)
    # ====================================================
    path('admin/courses/list/', AdminCourseListView.as_view(), name='admin-course-list'),
    path('admin/courses/add/', AdminCourseCreateView.as_view(), name='admin-course-add'),
    path('admin/instructors/add/', AdminInstructorCreateView.as_view(), name='admin-instructor-add'), # ✅ المسار الجديد لإضافة محاضر
    path('admin/notifications/send/', NotificationCreateView.as_view(), name='admin-notification-send'),
    path('admin/students/', AdminStudentListView.as_view(), name='admin-student-list'),
    path('admin/students/<int:pk>/', AdminStudentDetailView.as_view(), name='admin-student-detail'),

    # ====================================================
    # 5. وظائف المحاضر (Instructor)
    # ====================================================
    path('instructor/my-courses/', InstructorCoursesListView.as_view(), name='instructor-my-courses'),
    path('instructor/courses/<int:course_id>/students/', CourseRegisteredStudentsView.as_view(), name='course-students'),
    path('instructor/grade/update/', InstructorGradeUpdateView.as_view(), name='instructor-grade-update'),
]