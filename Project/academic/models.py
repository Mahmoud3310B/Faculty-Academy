# academic/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# ===================================================================
# 1. جدول المحاضرين (Instructor)
# ===================================================================
class Instructor(models.Model):
    # ربط المحاضر بكائن المستخدم الأساسي في Django
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"Instructor: {self.user.username}"

# ===================================================================
# 2. جدول الطالب (Student)
# ===================================================================
class Student(models.Model):
    # ربط الطالب بكائن المستخدم الأساسي في Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=20, unique=True)
    major = models.CharField(max_length=100)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    # لتحديد ما إذا كان الطالب دفع الرسوم أم لا (يؤثر على التسجيل)
    fees_paid_status = models.BooleanField(default=False) 

    def __str__(self):
        return f"Student: {self.user.username} ({self.national_id})"

# ===================================================================
# 3. جدول المواد (Course)
# ===================================================================
class Course(models.Model):
    LEVEL_CHOICES = (
        ('100', 'المستوى الأول'),
        ('200', 'المستوى الثاني'),
        ('300', 'المستوى الثالث'),
        ('400', 'المستوى الرابع'),
    )

    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=255)
    credit_hours = models.IntegerField(default=3)
    department = models.CharField(max_length=100)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='100')
    # حقل سعة المادة (تم تصحيحه من "max_seats" في ملف admin.py إلى هذا الاسم)
    capacity = models.IntegerField(default=30) 
    # علاقة مفتاح خارجي (ForeignKey) مع Instructor
    instructor = models.ForeignKey(
        Instructor, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='courses_taught'
    )
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

# ===================================================================
# 4. جدول أوقات المواد (CourseTime)
# ===================================================================
class CourseTime(models.Model):
    DAYS_OF_WEEK = (
        ('SUN', 'الأحد'),
        ('MON', 'الإثنين'),
        ('TUE', 'الثلاثاء'),
        ('WED', 'الأربعاء'),
        ('THU', 'الخميس'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='times')
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100, default='G-101')

    class Meta:
        # منع تكرار نفس المادة في نفس اليوم والوقت
        unique_together = ('course', 'day_of_week', 'start_time')
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.course.course_code} on {self.day_of_week} from {self.start_time.strftime('%H:%M')} to {self.end_time.strftime('%H:%M')}"

# ===================================================================
# 5. جدول التسجيل (Registration)
# ===================================================================
class Registration(models.Model):
    STATUS_CHOICES = (
        ('Registered', 'مسجل'),
        ('Dropped', 'منسحب'),
        ('Completed', 'مكتمل'),
        ('Failed', 'فشل'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='registrations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=50, default='Fall 2025')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Registered')
    final_grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # لا يمكن للطالب أن يسجل نفس المادة في نفس الفصل أكثر من مرة
        unique_together = ('student', 'course', 'semester')
        
    def __str__(self):
        return f"{self.student.user.username} registered in {self.course.course_code}"

# ===================================================================
# 6. جدول المدفوعات (Payment)
# ===================================================================
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('Pending', 'معلق'),
        ('Completed', 'مكتمل'),
        ('Failed', 'فشل'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment of {self.amount} by {self.student.user.username}"

# ===================================================================
# 7. جدول الإشعارات (Notification)
# ===================================================================
class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    # يمكن ربط الإشعار بمستخدم محدد، أو تركه فارغاً ليكون إشعاراً عاماً
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title