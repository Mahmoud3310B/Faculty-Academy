# academic/admin.py

from django.contrib import admin
from django.contrib.auth.models import User
from .models import Student, Instructor, Course, CourseTime, Registration, Payment, Notification

# -----------------------------------------------------
# 1. تخصيص جدول المحاضرين (Instructor)
# -----------------------------------------------------
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'employee_id', 'department', 'course_count')
    list_filter = ('department',)
    search_fields = ('user__username', 'employee_id')
    raw_id_fields = ('user',) 
    
    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'اسم المستخدم'

    def course_count(self, obj):
        return obj.courses_taught.count()
    course_count.short_description = 'عدد المواد'

# -----------------------------------------------------
# 2. تخصيص جدول الطلاب (Student)
# -----------------------------------------------------
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'national_id', 'major', 'gpa', 'fees_paid_status')
    list_filter = ('major', 'fees_paid_status')
    search_fields = ('user__username', 'national_id', 'major')
    raw_id_fields = ('user',) 
    
    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'اسم المستخدم'
    
    def fees_paid_status(self, obj):
        return obj.fees_paid_status
    fees_paid_status.boolean = True
    fees_paid_status.short_description = 'حالة الرسوم'
    
# -----------------------------------------------------
# 3. تخصيص جدول المواد (Course)
# -----------------------------------------------------
class CourseTimeInline(admin.TabularInline):
    model = CourseTime
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    # ✅ السطر المصحح الذي يحل مشكلة SystemCheckError
    list_display = ('course_code', 'course_name', 'instructor_name', 'credit_hours', 'capacity') 
    
    list_filter = ('department', 'level')
    search_fields = ('course_code', 'course_name')
    raw_id_fields = ('instructor',)
    inlines = [CourseTimeInline]

    def instructor_name(self, obj):
        return obj.instructor.user.username if obj.instructor else 'لا يوجد'
    instructor_name.short_description = 'المحاضر'

# -----------------------------------------------------
# 4. تخصيص جدول أوقات المواد (CourseTime)
# -----------------------------------------------------
class CourseTimeAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'day_of_week', 'start_time', 'end_time', 'location')
    list_filter = ('day_of_week', 'location')
    raw_id_fields = ('course',)
    
    def course_code(self, obj):
        return obj.course.course_code
    course_code.short_description = 'رمز المادة'

# -----------------------------------------------------
# 5. تخصيص جدول التسجيل (Registration)
# -----------------------------------------------------
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'course_code', 'semester', 'status', 'final_grade')
    list_filter = ('semester', 'status')
    search_fields = ('student__user__username', 'course__course_code')
    raw_id_fields = ('student', 'course') 
    
    def student_name(self, obj):
        return obj.student.user.username
    student_name.short_description = 'الطالب'
    
    def course_code(self, obj):
        return obj.course.course_code
    course_code.short_description = 'رمز المادة'


# -----------------------------------------------------
# 6. تخصيص جدول الدفع (Payment)
# -----------------------------------------------------
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'amount', 'transaction_id', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('transaction_id', 'student__user__username')
    readonly_fields = ('transaction_id', 'created_at')
    
    def student_name(self, obj):
        return obj.student.user.username
    student_name.short_description = 'الطالب'

# -----------------------------------------------------
# 7. تخصيص جدول الإشعارات (Notification)
# -----------------------------------------------------
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'message_snippet', 'user_username', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username')
    raw_id_fields = ('user',)

    def message_snippet(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_snippet.short_description = 'مقتطف من الرسالة'

    def user_username(self, obj):
        return obj.user.username if obj.user else 'عام'
    user_username.short_description = 'للمستخدم'

# -----------------------------------------------------
# تسجيل النماذج المخصصة
# -----------------------------------------------------
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseTime, CourseTimeAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Notification, NotificationAdmin)