// static/js/login.js

// المسار الأساسي لنقاط API (تأكد من مطابقته لمنفذ خادم Django الخاص بك)
const API_BASE_URL = 'http://127.0.0.1:8000/api/';

// يتم ربط دالة handleLogin بحدث إرسال النموذج (submit)
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
});

function handleLogin(event) {
    event.preventDefault(); 

    // جلب قيم الحقول باستخدام المعرفات (IDs)
    const username = document.getElementById('username').value;
    const password = document.getElementById('passwordField').value;
    const messageElement = document.getElementById('message');

    // عرض رسالة "جاري التحقق..." مؤقتة
    messageElement.textContent = 'جاري التحقق من البيانات...';
    messageElement.style.color = '#007bff';

    fetch(API_BASE_URL + 'token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            // يتم إرسال البيانات بـ 'username' و 'password' كما يتوقع Django
            username: username,
            password: password
        })
    })
    // قراءة الرد وتحويله إلى JSON مع الحفاظ على كود الحالة (status code)
    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(({ status, body }) => {
        if (status === 200) {
            // ✅ نجاح تسجيل الدخول
            
            // 1. تخزين التوكن والدور في التخزين المحلي (Local Storage)
            localStorage.setItem('accessToken', body.access);
            localStorage.setItem('refreshToken', body.refresh);
            localStorage.setItem('userRole', body.role); // 'Student', 'Instructor', 'Administrator'

            messageElement.textContent = 'تم تسجيل الدخول بنجاح! جاري التوجيه...';
            messageElement.style.color = 'green';
            
            // 2. التوجيه إلى الصفحة الصحيحة بناءً على الرد من الـ Backend
            const redirectUrl = body.redirect_url || '/index.html'; 
            window.location.href = redirectUrl; 

        } else {
            // ❌ فشل تسجيل الدخول
            const errorMsg = body.detail || 'اسم المستخدم أو كلمة المرور غير صحيحة.';
            messageElement.textContent = `خطأ: ${errorMsg}`;
            messageElement.style.color = 'red';
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        messageElement.textContent = 'خطأ في الاتصال بالخادم. تأكد من تشغيل Django.';
        messageElement.style.color = 'red';
    });
}