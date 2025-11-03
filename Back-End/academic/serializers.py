# academic/serializers.py (المُصحح)

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # ✅ تم استيراد الكلاس الصحيح
from .models import Student, Instructor, Course, Registration, Payment, Notification

# ----------------- JWT و Auth (المُصحح) -----------------

# 🚨 أهم تصحيح: يرث الآن من الكلاس الأساسي لـ Simple JWT لضمان إنشاء الـ Token بشكل صحيح.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    # لا حاجة لتعريف validate() هنا، الكلاس الأب يقوم بكل شيء.
    
    @classmethod
    def get_token(cls, user):
        # 1. إنشاء التوكن الأساسي (يتضمن access و refresh)
        token = super().get_token(user)

        # 2. إضافة الدور (Role) إلى الحمولة (Payload)
        if user.is_superuser:
            role = 'Administrator'
        elif Instructor.objects.filter(user=user).exists():
            role = 'Instructor'
        elif Student.objects.filter(user=user).exists():
            role = 'Student'
        else:
            role = 'User'
        
        token['role'] = role
        return token

# ----------------- الإدارة والبيانات -----------------

class StudentManagementSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'username', 'national_id', 'major', 'gpa', 'fees_paid_status']
        read_only_fields = ['national_id']

class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.user.username', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'student_name', 'amount', 'transaction_id', 'status', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'created_at', 'is_read']
        read_only_fields = ['created_at', 'is_read']

# المسلسل لإنشاء المحاضر
class InstructorCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Instructor
        fields = ['id', 'username', 'password', 'employee_id', 'department']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        
        try:
            user = User.objects.create_user(username=username, password=password)
        except Exception:
             raise serializers.ValidationError({"username": "اسم المستخدم هذا مستخدم بالفعل."})

        instructor = Instructor.objects.create(user=user, **validated_data)
        return instructor