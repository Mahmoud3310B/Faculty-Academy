# academic/views.py (الكود الكامل والمدمج)

import uuid
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db.models import Q 
from django.utils import timezone

from .models import Course, Student, Registration, Instructor, Payment, Notification
from .serializers import (
    CustomTokenObtainPairSerializer, 
    CourseSerializer, 
    PaymentSerializer, 
    StudentManagementSerializer,
    NotificationSerializer,
    InstructorCreateSerializer, # ✅ المسلسل الجديد لإضافة محاضر
) 
from .permissions import IsAdministrator, IsInstructor

# ====================================================================
# 1. المصادقة (Authentication)
# ====================================================================
class LoginView(TokenObtainPairView):
    """ نقطة API لتسجيل الدخول وإرجاع التوكن والدور. """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # بعد النجاح، نحدد دور المستخدم لإرساله للواجهة الأمامية
            user = self.get_serializer(data=request.data).user
            role = 'Student'
            if user.is_superuser or user.is_staff:
                role = 'Administrator'
            elif hasattr(user, 'instructor'):
                role = 'Instructor'
                
            response.data['role'] = role
            # مسار التوجيه بعد تسجيل الدخول
            response.data['redirect_url'] = '/management.html' if role in ['Administrator', 'Instructor'] else '/index.html'
            
        return response

# ====================================================================
# 2. وظائف الطالب (Student Features)
# ====================================================================

class CourseListView(generics.ListAPIView):
    """ عرض قائمة بالمواد المتاحة للتسجيل. """
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Course.objects.all().select_related('instructor__user')

class RegisterCourseView(APIView):
    """ تسجيل الطالب في مادة دراسية. """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')

        try:
            student = Student.objects.get(user=request.user)
            course = Course.objects.get(pk=course_id)

            # 1. التحقق من حالة دفع الرسوم
            if not student.fees_paid_status:
                return Response({'detail': 'يجب عليك دفع الرسوم أولاً لتتمكن من التسجيل.'}, status=status.HTTP_403_FORBIDDEN)

            # 2. التحقق من عدم تكرار التسجيل
            if Registration.objects.filter(student=student, course=course).exists():
                return Response({'detail': 'أنت مسجل بالفعل في هذه المادة.'}, status=status.HTTP_400_BAD_REQUEST)

            # 3. إنشاء سجل التسجيل
            Registration.objects.create(student=student, course=course)

            return Response({'detail': 'تم التسجيل في المادة بنجاح.'}, status=status.HTTP_201_CREATED)

        except Student.DoesNotExist:
            return Response({'detail': 'بيانات الطالب غير موجودة.'}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({'detail': 'المادة غير موجودة.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f'حدث خطأ: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CancelRegistrationView(APIView):
    """ ✨ الجديدة: نقطة API لإلغاء تسجيل مادة. """
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        course_id = request.data.get('course_id') 

        if not course_id:
            return Response({'detail': 'معرّف المادة (course_id) مطلوب.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(user=request.user)
            course = Course.objects.get(pk=course_id)

            # البحث عن سجل التسجيل الذي يربط الطالب بالمادة وحذفه
            registration = Registration.objects.get(
                student=student, 
                course=course, 
                status='Pending'
            )
            registration.delete()

            return Response({'detail': 'تم إلغاء التسجيل في المادة بنجاح.'}, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({'detail': 'بيانات الطالب غير موجودة.'}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({'detail': 'المادة غير موجودة.'}, status=status.HTTP_404_NOT_FOUND)
        except Registration.DoesNotExist:
            return Response({'detail': 'أنت لست مسجلاً في هذه المادة أو لا يمكن إلغاء تسجيلها حاليًا.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'حدث خطأ غير متوقع: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentScheduleView(APIView):
    """ عرض جدول الطالب الدراسي (المواد المسجل بها). """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
            
            registered_courses = Course.objects.filter(
                registration__student=student, 
                registration__status='Pending'
            ).select_related('instructor__user')
            
            serializer = CourseSerializer(registered_courses, many=True)
            return Response(serializer.data)

        except Student.DoesNotExist:
            return Response({'detail': 'بيانات الطالب غير موجودة.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f'حدث خطأ: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NotificationListView(generics.ListAPIView):
    """ عرض قائمة الإشعارات للطالب (العامة والخاصة). """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(Q(user=None) | Q(user=self.request.user)).order_by('-created_at')

# ====================================================================
# 3. المدفوعات (Payments)
# ====================================================================

class InitiatePaymentView(APIView):
    """ بدء عملية دفع جديدة. """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        amount = request.data.get('amount')
        
        try:
            student = Student.objects.get(user=request.user)
            transaction_id = str(uuid.uuid4()) 
            
            payment = Payment.objects.create(
                student=student,
                amount=amount,
                transaction_id=transaction_id,
                status='Pending'
            )
            
            serializer = PaymentSerializer(payment)
            return Response({'detail': 'تم إنشاء عملية الدفع بنجاح.', 'payment': serializer.data}, status=status.HTTP_201_CREATED)
            
        except Student.DoesNotExist:
            return Response({'detail': 'الطالب غير موجود.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f'فشل في بدء عملية الدفع: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentUpdateView(APIView):
    """ تحديث حالة الدفع إلى 'Completed' (محاكاة لإتمام الدفع). """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        
        try:
            student = Student.objects.get(user=request.user)
            payment = Payment.objects.get(
                transaction_id=transaction_id, 
                student=student,
                status='Pending'
            )
            
            payment.status = 'Completed'
            payment.paid_at = timezone.now()
            payment.save()
            
            # تحديث حالة دفع الرسوم للطالب
            student.fees_paid_status = True
            student.save()
            
            return Response({'detail': 'تم إتمام عملية الدفع بنجاح وتحديث حالة الطالب.'}, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({'detail': 'الطالب غير موجود.'}, status=status.HTTP_404_NOT_FOUND)
        except Payment.DoesNotExist:
            return Response({'detail': 'لم يتم العثور على عملية دفع معلقة بهذا المعرّف.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f'فشل في تحديث حالة الدفع: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentHistoryView(generics.ListAPIView):
    """ عرض سجل الدفعات السابقة للطالب. """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return Payment.objects.filter(student=student).order_by('-created_at')
        except Student.DoesNotExist:
            return Payment.objects.none() 

# ====================================================================
# 4. وظائف المسؤول (Admin Features)
# ====================================================================

class AdminCourseListView(generics.ListAPIView):
    """ عرض قائمة بجميع المواد في النظام (للمسؤول). """
    serializer_class = CourseSerializer
    permission_classes = [IsAdministrator]
    
    def get_queryset(self):
        return Course.objects.all().select_related('instructor__user')

class AdminCourseCreateView(generics.CreateAPIView):
    """ إنشاء مادة جديدة (للمسؤول). """
    serializer_class = CourseSerializer
    permission_classes = [IsAdministrator]

class AdminInstructorCreateView(generics.CreateAPIView):
    """ ✨ الجديدة: نقطة API لإنشاء حساب محاضر جديد (للمسؤول). """
    serializer_class = InstructorCreateSerializer
    permission_classes = [IsAdministrator] 
    
class AdminStudentListView(generics.ListAPIView):
    """ عرض قائمة بجميع الطلاب في النظام (للمسؤول). """
    serializer_class = StudentManagementSerializer
    permission_classes = [IsAdministrator]
    
    def get_queryset(self):
        return Student.objects.all().select_related('user')

class AdminStudentDetailView(generics.RetrieveUpdateAPIView):
    """ عرض وتحديث تفاصيل طالب معين (للمسؤول). """
    serializer_class = StudentManagementSerializer
    permission_classes = [IsAdministrator]
    queryset = Student.objects.all()
    lookup_field = 'pk' 

class NotificationCreateView(generics.CreateAPIView):
    """ إرسال إشعار جديد (للمسؤول). """
    serializer_class = NotificationSerializer
    permission_classes = [IsAdministrator]

    def perform_create(self, serializer):
        # حفظ الإشعار كإشعار عام
        serializer.save(user=None) 

# ====================================================================
# 5. وظائف المحاضر (Instructor Features)
# ====================================================================

class InstructorCoursesListView(APIView):
    """ عرض قائمة بالمواد التي يقوم المحاضر بتدريسها. """
    permission_classes = [IsInstructor]

    def get(self, request):
        try:
            instructor = Instructor.objects.get(user=request.user)
            my_courses = Course.objects.filter(instructor=instructor)
            serializer = CourseSerializer(my_courses, many=True)
            return Response(serializer.data)
        except Instructor.DoesNotExist:
            return Response({'detail': 'بيانات المحاضر غير موجودة.'}, status=status.HTTP_404_NOT_FOUND)


class CourseRegisteredStudentsView(APIView):
    """ عرض قائمة بأسماء الطلاب المسجلين في مادة معينة يدرسها المحاضر. """
    permission_classes = [IsInstructor]

    def get(self, request, course_id):
        try:
            instructor = Instructor.objects.get(user=request.user)
            course = Course.objects.get(pk=course_id, instructor=instructor)

            registered_students = Student.objects.filter(
                registration__course=course
            ).select_related('user')
            
            serializer = StudentManagementSerializer(registered_students, many=True)
            return Response(serializer.data)

        except Instructor.DoesNotExist:
            return Response({'detail': 'غير مصرح لك بالوصول لبيانات هذه المادة.'}, status=status.HTTP_403_FORBIDDEN)
        except Course.DoesNotExist:
            return Response({'detail': 'المادة غير موجودة أو ليست ضمن موادك.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f'حدث خطأ: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InstructorGradeUpdateView(APIView):
    """ تحديث الدرجة النهائية لطالب في مادة معينة. """
    permission_classes = [IsInstructor]

    def post(self, request):
        try:
            instructor = Instructor.objects.get(user=request.user)
            student_id = request.data.get('student_id')
            course_id = request.data.get('course_id')
            final_grade = request.data.get('final_grade')
            
            course = Course.objects.get(pk=course_id, instructor=instructor)
            student = Student.objects.get(pk=student_id)

            registration = Registration.objects.get(student=student, course=course)
            
            if final_grade is not None:
                registration.final_grade = final_grade
                registration.status = 'Completed' 
                registration.save()
            
            return Response({'detail': 'تم تحديث الدرجة بنجاح.'}, status=status.HTTP_200_OK)

        except Instructor.DoesNotExist:
            return Response({'detail': 'غير مصرح لك بتعديل هذه الدرجة.'}, status=status.HTTP_403_FORBIDDEN)
        except (Course.DoesNotExist, Student.DoesNotExist, Registration.DoesNotExist):
            return Response({'detail': 'خطأ: لم يتم العثور على المادة أو الطالب أو سجل التسجيل.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f'حدث خطأ غير متوقع: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)