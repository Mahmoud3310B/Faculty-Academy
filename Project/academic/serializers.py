
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # ✅ تم استيراد الكلاس الصحيح
from .models import Student, Instructor, Course, Registration, Payment, Notification


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

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