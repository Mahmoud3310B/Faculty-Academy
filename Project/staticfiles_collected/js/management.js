// static/js/management.js

// 🛑 المسار الأساسي (تأكد من مطابقته لمنفذ خادم Django الخاص بك)
const API_BASE_URL = 'http://127.0.0.1:8000/api/'; 

// -------------------------------------------------------------------
// 1. إدارة الجلسة والمصادقة (Auth & Session Management)
// -------------------------------------------------------------------

/**
 * دالة تسجيل الخروج: مسح البيانات وإعادة التوجيه إلى صفحة الدخول.
 */
function logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('userRole');
    window.location.href = '/login.html';
}

/**
 * دالة لتحديث الـ Access Token باستخدام الـ Refresh Token.
 * @returns {string|null} Access Token الجديد أو null في حالة الفشل.
 */
async function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) return null;

    const response = await fetch(API_BASE_URL + 'token/refresh/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('accessToken', data.access);
        return data.access;
    } else {
        // فشل التحديث: يجب تسجيل الخروج
        logout();
        return null;
    }
}

/**
 * دالة محمية لإرسال الطلبات إلى الـ API، مع محاولة تحديث الـ Token عند فشل المصادقة (401).
 */
async function fetchProtectedData(endpoint, method = 'GET', body = null, isRetry = false) {
    let accessToken = localStorage.getItem('accessToken');
    
    if (!accessToken) { 
        logout(); 
        return null; 
    }

    const url = API_BASE_URL + endpoint;

    const requestOptions = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`,
        },
    };

    if (body) {
        requestOptions.body = JSON.stringify(body);
    }

    let response = await fetch(url, requestOptions);

    if (response.status === 401 && !isRetry) {
        // فشل المصادقة: حاول التحديث وإعادة الطلب
        const newAccessToken = await refreshAccessToken();
        if (newAccessToken) {
            // تحديث التوكن في الـ Headers وإعادة المحاولة
            requestOptions.headers['Authorization'] = `Bearer ${newAccessToken}`;
            response = await fetch(url, requestOptions);
        } else {
            return null;
        }
    }
    
    if (response.ok) {
        // بعض الطلبات (مثل POST/PUT/DELETE) قد لا تعيد جسماً (Body)
        if (response.status === 204 || response.headers.get('content-length') === '0') {
            return { status: response.status, body: null };
        }
        const data = await response.json();
        return { status: response.status, body: data };
    } else {
        let errorBody = null;
        try {
            errorBody = await response.json();
        } catch (e) {
            // لا يوجد JSON Body
        }
        return { status: response.status, body: errorBody };
    }
}

// -------------------------------------------------------------------
// 2. وظائف تهيئة الصفحة والتحقق من الصلاحيات
// -------------------------------------------------------------------

async function initializeManagementPage() {
    const role = localStorage.getItem('userRole');
    const loadingMessage = document.getElementById('loadingMessage');
    const forbiddenMessage = document.getElementById('forbiddenMessage');
    const adminSection = document.getElementById('adminSection');
    const instructorSection = document.getElementById('instructorSection');
    const roleDisplay = document.getElementById('userRoleDisplay');

    // إخفاء رسالة التحميل
    if (loadingMessage) loadingMessage.style.display = 'none';

    if (!role || role === 'Student') {
        // دور غير مصرح له بالدخول لصفحة الإدارة
        if (forbiddenMessage) {
            forbiddenMessage.style.display = 'block';
            setTimeout(logout, 3000); // توجيه للخروج بعد 3 ثوان
        } else {
             logout();
        }
        return;
    }
    
    // عرض الدور في شريط التنقل
    if (roleDisplay) roleDisplay.textContent = role;
    
    // إخفاء جميع الأقسام افتراضياً
    if (adminSection) adminSection.style.display = 'none';
    if (instructorSection) instructorSection.style.display = 'none';

    if (role === 'Administrator') {
        if (adminSection) adminSection.style.display = 'block';
        await loadAdminData();
        
        // ربط النماذج بمعالجات الأحداث
        document.getElementById('addCourseForm')?.addEventListener('submit', handleAddCourse);
        document.getElementById('addInstructorForm')?.addEventListener('submit', handleAddInstructor);
        document.getElementById('sendNotificationForm')?.addEventListener('submit', handleSendNotification);

    } else if (role === 'Instructor') {
        if (instructorSection) instructorSection.style.display = 'block';
        await loadInstructorData();
    } 
}

// -------------------------------------------------------------------
// 3. وظائف معالجة نماذج المسؤول (Admin Handlers)
// -------------------------------------------------------------------

/**
 * معالجة نموذج إضافة مادة جديدة.
 */
async function handleAddCourse(event) {
    event.preventDefault();

    const messageElement = document.getElementById('courseMessage'); 
    messageElement.textContent = 'جاري إضافة المادة...';
    messageElement.className = 'text-info';

    try {
        // جلب القيم من العناصر باستخدام المعرّفات (IDs)
        const courseCode = document.getElementById('courseCode').value;
        const courseName = document.getElementById('courseName').value;
        // يجب تحويلها إلى أرقام
        const creditHours = parseInt(document.getElementById('creditHours').value);
        const instructorId = parseInt(document.getElementById('courseInstructor').value); 
        
        const courseData = {
            course_code: courseCode,
            course_name: courseName,
            credit_hours: creditHours,
            instructor: instructorId,
        };

        const response = await fetchProtectedData('admin/courses/add/', 'POST', courseData);

        if (response && response.status === 201) {
            // ✅ نجاح الإضافة
            messageElement.textContent = `✅ تم إضافة المادة (${courseName}) بنجاح!`;
            messageElement.className = 'text-success fw-bold';
            await loadAdminCourses(); // تحديث القائمة
            document.getElementById('addCourseForm').reset();
        } else if (response && response.body) {
            // ❌ فشل التحقق (400 Bad Request)
            let errorMsg = '❌ فشل في الإضافة.';
            if (response.body.course_code && Array.isArray(response.body.course_code) && response.body.course_code.some(msg => msg.includes('already exists'))) {
                errorMsg = `❌ فشل الإضافة: رمز المادة مستخدم بالفعل.`;
            } else if (response.body.detail) {
                errorMsg = `❌ فشل الإضافة: ${response.body.detail}`;
            } else {
                 // عرض أول رسالة خطأ غير مُعالجة
                errorMsg = `❌ فشل الإضافة: ${JSON.stringify(response.body)}`;
            }
            
            messageElement.textContent = errorMsg;
            messageElement.className = 'text-danger fw-bold';
        } else {
             messageElement.textContent = '❌ فشل الاتصال بالخادم.';
             messageElement.className = 'text-danger';
        }

    } catch (error) {
        console.error("Error in handleAddCourse:", error);
        messageElement.textContent = '❌ خطأ برمجي: يرجى مراجعة console.';
        messageElement.className = 'text-danger';
    }
}

/**
 * معالجة نموذج إضافة محاضر جديد (Instructor).
 */
async function handleAddInstructor(event) {
    event.preventDefault();

    const messageElement = document.getElementById('instructorMessage'); 
    messageElement.textContent = 'جاري إضافة المحاضر...';
    messageElement.className = 'text-info';

    try {
        const instUsername = document.getElementById('instUsername').value;
        const instPassword = document.getElementById('instPassword').value;
        const instEmployeeId = document.getElementById('instEmployeeId').value;
        const instDepartment = document.getElementById('instDepartment').value;
        
        const instructorData = {
            username: instUsername,
            password: instPassword,
            employee_id: instEmployeeId,
            department: instDepartment,
        };

        // المسار الجديد الذي تم إضافته في academic/urls.py
        const response = await fetchProtectedData('admin/instructors/add/', 'POST', instructorData);

        if (response && response.status === 201) {
            messageElement.textContent = `✅ تم إضافة المحاضر (${instUsername}) بنجاح!`;
            messageElement.className = 'text-success fw-bold';
            document.getElementById('addInstructorForm').reset();
            // إعادة تحميل بيانات المسؤول لتحديث قائمة المحاضرين في نموذج إضافة المواد
            await loadAdminData(); 
        } else if (response && response.body) {
            let errorMsg = '❌ فشل في الإضافة.';
            if (response.body.username && Array.isArray(response.body.username)) {
                errorMsg = `❌ فشل الإضافة: اسم المستخدم مستخدم بالفعل.`;
            } else if (response.body.employee_id && Array.isArray(response.body.employee_id)) {
                errorMsg = `❌ فشل الإضافة: رقم الموظف مستخدم بالفعل.`;
            } else if (response.body.detail) {
                errorMsg = `❌ فشل الإضافة: ${response.body.detail}`;
            } else {
                errorMsg = `❌ فشل الإضافة: ${JSON.stringify(response.body)}`;
            }
            messageElement.textContent = errorMsg;
            messageElement.className = 'text-danger fw-bold';
        } else {
             messageElement.textContent = '❌ فشل الاتصال بالخادم.';
             messageElement.className = 'text-danger';
        }

    } catch (error) {
        console.error("Error in handleAddInstructor:", error);
        messageElement.textContent = '❌ خطأ برمجي: يرجى مراجعة console.';
        messageElement.className = 'text-danger';
    }
}

/**
 * معالجة نموذج إرسال إشعار عام.
 */
async function handleSendNotification(event) {
    event.preventDefault();

    const messageElement = document.getElementById('notificationMessage'); 
    messageElement.textContent = 'جاري إرسال الإشعار...';
    messageElement.className = 'text-info';

    try {
        const title = document.getElementById('notifTitle').value;
        const message = document.getElementById('notifMessage').value;

        const notifData = { title, message };

        const response = await fetchProtectedData('admin/notifications/send/', 'POST', notifData);

        if (response && response.status === 201) {
            messageElement.textContent = `✅ تم إرسال الإشعار العام بنجاح!`;
            messageElement.className = 'text-success fw-bold';
            document.getElementById('sendNotificationForm').reset();
        } else {
            messageElement.textContent = '❌ فشل في إرسال الإشعار.';
            messageElement.className = 'text-danger fw-bold';
        }

    } catch (error) {
        console.error("Error in handleSendNotification:", error);
        messageElement.textContent = '❌ خطأ برمجي: يرجى مراجعة console.';
        messageElement.className = 'text-danger';
    }
}


// -------------------------------------------------------------------
// 4. وظائف جلب وعرض بيانات المسؤول (Admin Display)
// -------------------------------------------------------------------

async function loadAdminData() {
    // جلب قائمة الطلاب
    await loadAdminStudents();
    // جلب قائمة المواد
    await loadAdminCourses();
    // جلب قائمة المحاضرين لملء الـ Select
    await loadInstructorsForSelect(); 
}

/**
 * جلب وعرض قائمة الطلاب.
 */
async function loadAdminStudents() {
    const response = await fetchProtectedData('admin/students/');
    const studentsTableBody = document.getElementById('studentsTableBody');
    const studentsCount = document.getElementById('studentsCount');
    
    if (!response || response.status !== 200) {
        studentsTableBody.innerHTML = '<tr><td colspan="6">فشل في تحميل بيانات الطلاب.</td></tr>';
        return;
    }

    const students = response.body;
    studentsCount.textContent = students.length;
    studentsTableBody.innerHTML = '';
    
    students.forEach((student, index) => {
        const row = studentsTableBody.insertRow();
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${student.username}</td>
            <td>${student.national_id}</td>
            <td>${student.major}</td>
            <td>${student.gpa}</td>
            <td><span class="badge bg-${student.fees_paid_status ? 'success' : 'danger'}">${student.fees_paid_status ? 'مدفوعة' : 'غير مدفوعة'}</span></td>
            <td>
                <button class="btn btn-sm btn-info" onclick="viewStudentDetails(${student.id})"><i class="bi bi-eye-fill"></i></button>
            </td>
        `;
    });
}

/**
 * جلب وعرض قائمة المواد (للمسؤول).
 */
async function loadAdminCourses() {
    const response = await fetchProtectedData('admin/courses/list/');
    const coursesTableBody = document.getElementById('adminCoursesTableBody');
    const coursesCount = document.getElementById('adminCoursesCount');

    if (!response || response.status !== 200) {
        coursesTableBody.innerHTML = '<tr><td colspan="4">فشل في تحميل بيانات المواد.</td></tr>';
        return;
    }

    const courses = response.body;
    coursesCount.textContent = courses.length;
    coursesTableBody.innerHTML = '';

    courses.forEach(course => {
        const row = coursesTableBody.insertRow();
        row.innerHTML = `
            <td>${course.course_code}</td>
            <td>${course.course_name}</td>
            <td>${course.credit_hours}</td>
            <td>${course.instructor_name || 'غير محدد'}</td>
        `;
    });
}


/**
 * جلب قائمة المحاضرين وملء قائمة الاختيار (Select) في نموذج إضافة مادة.
 */
async function loadInstructorsForSelect() {
    // **ملاحظة:** بما أنه لا يوجد API مخصص للمحاضرين، نستخدم قائمة الطلاب مؤقتاً لملء الـ SELECT.
    const response = await fetchProtectedData('admin/students/'); 
    const instructorSelect = document.getElementById('courseInstructor');
    
    if (!response || response.status !== 200) {
        instructorSelect.innerHTML = '<option value="">فشل تحميل المحاضرين</option>';
        return;
    }
    
    // إفراغ القائمة
    instructorSelect.innerHTML = '<option value="">اختر المحاضر...</option>';

    const students = response.body; 
    students.forEach(student => {
        const option = document.createElement('option');
        // هنا نستخدم ID الطالب كـ ID المحاضر مؤقتاً لغرض الاختبار
        option.value = student.id; 
        option.textContent = student.username;
        instructorSelect.appendChild(option);
    });
}


// -------------------------------------------------------------------
// 5. وظائف جلب وعرض بيانات المحاضر (Instructor Display)
// -------------------------------------------------------------------

async function loadInstructorData() {
    const response = await fetchProtectedData('instructor/my-courses/');
    const coursesTableBody = document.getElementById('instructorCoursesTableBody');
    const coursesCount = document.getElementById('instructorCoursesCount');

    if (!response || response.status !== 200) {
        coursesTableBody.innerHTML = '<tr><td colspan="5">فشل في تحميل موادك.</td></tr>';
        return;
    }

    const courses = response.body;
    coursesCount.textContent = courses.length;
    coursesTableBody.innerHTML = '';

    courses.forEach(course => {
        const row = coursesTableBody.insertRow();
        row.innerHTML = `
            <td>${course.course_code}</td>
            <td>${course.course_name}</td>
            <td>${course.credit_hours}</td>
            <td>(جارٍ التحميل...)</td> <td>
                <button class="btn btn-sm btn-primary" onclick="loadCourseStudents(${course.id}, '${course.course_name}')">
                    <i class="bi bi-people-fill me-1"></i> إدارة الطلاب
                </button>
            </td>
        `;
    });
}

let currentCourseId = null;

/**
 * جلب وعرض الطلاب المسجلين في مادة معينة.
 */
async function loadCourseStudents(courseId, courseName) {
    const response = await fetchProtectedData(`instructor/courses/${courseId}/students/`);
    const studentsTableBody = document.getElementById('courseStudentsTableBody');
    const courseStudentsSection = document.getElementById('courseStudentsSection');
    const currentCourseName = document.getElementById('currentCourseName');
    
    currentCourseId = courseId;
    courseStudentsSection.style.display = 'block';
    currentCourseName.textContent = courseName;
    studentsTableBody.innerHTML = '<tr><td colspan="5">جاري التحميل...</td></tr>';


    if (!response || response.status !== 200) {
        studentsTableBody.innerHTML = '<tr><td colspan="5">فشل في تحميل بيانات الطلاب.</td></tr>';
        return;
    }

    const students = response.body;
    studentsTableBody.innerHTML = '';

    if (students.length === 0) {
         studentsTableBody.innerHTML = '<tr><td colspan="5" class="text-center">لم يتم تسجيل أي طالب في هذه المادة بعد.</td></tr>';
         return;
    }

    students.forEach(student => {
        // افتراضياً: الدرجة مخزنة في حقل إضافي اسمه final_grade (يجب تعديل الـ Serializer/View ليجلبها)
        const currentGrade = student.final_grade || ''; 
        
        const row = studentsTableBody.insertRow();
        row.id = `student-row-${student.id}`;
        row.innerHTML = `
            <td>${student.username}</td>
            <td>${student.national_id}</td>
            <td>${student.major}</td>
            <td>
                <input type="number" class="form-control form-control-sm" id="grade-${student.id}" value="${currentGrade}" min="0" max="100" style="width: 80px;">
            </td>
            <td>
                <button class="btn btn-sm btn-success" onclick="handleGradeUpdate(${student.id})">
                    <i class="bi bi-save-fill"></i> حفظ
                </button>
            </td>
        `;
    });
}

/**
 * معالجة تحديث الدرجة النهائية للطالب.
 */
async function handleGradeUpdate(studentId) {
    const gradeInput = document.getElementById(`grade-${studentId}`);
    const finalGrade = parseInt(gradeInput.value);
    const messageElement = document.getElementById('gradeUpdateMessage');

    if (isNaN(finalGrade) || finalGrade < 0 || finalGrade > 100) {
        messageElement.textContent = '❌ يجب إدخال درجة صالحة بين 0 و 100.';
        messageElement.className = 'text-danger fw-bold';
        return;
    }

    if (!currentCourseId) {
        messageElement.textContent = '❌ خطأ: لم يتم تحديد المادة.';
        messageElement.className = 'text-danger fw-bold';
        return;
    }

    messageElement.textContent = 'جاري حفظ الدرجة...';
    messageElement.className = 'text-info';

    const gradeData = {
        student_id: studentId,
        course_id: currentCourseId,
        final_grade: finalGrade,
    };

    const response = await fetchProtectedData('instructor/grade/update/', 'POST', gradeData);
    
    if (response && response.status === 200) {
        messageElement.textContent = `✅ تم حفظ الدرجة ${finalGrade} للطالب بنجاح.`;
        messageElement.className = 'text-success fw-bold';
        // لا حاجة لإعادة تحميل الصفحة، فقط عرض الرسالة
    } else {
        let errorMsg = '❌ فشل في حفظ الدرجة.';
        if (response && response.body && response.body.detail) {
            errorMsg = `❌ فشل في حفظ الدرجة: ${response.body.detail}`;
        }
        messageElement.textContent = errorMsg;
        messageElement.className = 'text-danger fw-bold';
    }
}