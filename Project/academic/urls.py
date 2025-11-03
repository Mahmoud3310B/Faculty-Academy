
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView 
from .views import (
    # Auth
    LoginView,
    # Student
    CourseListView, RegisterCourseView, CancelRegistrationView, StudentScheduleView, NotificationListView,
    InitiatePaymentView, PaymentUpdateView, PaymentHistoryView,
    # Admin
    AdminCourseCreateView, AdminCourseListView, AdminStudentListView, AdminStudentDetailView, AdminInstructorCreateView, NotificationCreateView,
    # Instructor
    InstructorCoursesListView, CourseRegisteredStudentsView, InstructorGradeUpdateView
)

urlpatterns = [
    # 1. AUTH & JWT
    path('token/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 2. STUDENT API (مسارات الطالب)
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('register/', RegisterCourseView.as_view(), name='course_register'),
    path('cancel/', CancelRegistrationView.as_view(), name='registration_cancel'),
    path('schedule/', StudentScheduleView.as_view(), name='student_schedule'),
    path('notifications/', NotificationListView.as_view(), name='student_notifications'),
    
    # Payments (المدفوعات)
    path('payments/initiate/', InitiatePaymentView.as_view(), name='payment_initiate'),
    path('payments/update/', PaymentUpdateView.as_view(), name='payment_update'),
    path('payments/history/', PaymentHistoryView.as_view(), name='payment_history'),

    # 3. ADMIN API (مسارات المسؤول)
    path('admin/courses/list/', AdminCourseListView.as_view(), name='admin_course_list'),
    path('admin/courses/add/', AdminCourseCreateView.as_view(), name='admin_course_create'),
    path('admin/instructors/add/', AdminInstructorCreateView.as_view(), name='admin_instructor_create'),
    path('admin/students/', AdminStudentListView.as_view(), name='admin_student_list'),
    path('admin/students/<int:pk>/', AdminStudentDetailView.as_view(), name='admin_student_detail'),
    path('admin/notifications/send/', NotificationCreateView.as_view(), name='admin_notification_send'),

    # 4. INSTRUCTOR API (مسارات المحاضر)
    path('instructor/my-courses/', InstructorCoursesListView.as_view(), name='instructor_courses'),
    path('instructor/courses/<int:course_id>/students/', CourseRegisteredStudentsView.as_view(), name='course_students'),
    path('instructor/grade/update/', InstructorGradeUpdateView.as_view(), name='instructor_grade_update'),
]