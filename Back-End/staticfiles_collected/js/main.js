// static/js/main.js (المحتوى الكامل)

document.addEventListener('DOMContentLoaded', function() {
    const htmlElement = document.documentElement;
    const themeToggle = document.getElementById('theme-toggle');
    const menuToggle = document.getElementById('menu-toggle');
    const wrapper = document.getElementById('wrapper');

    // ------------------------------------------------------------------
    // 1. وظيفة تبديل الثيم ومنطق الشريط الجانبي (كما كانت)
    // ------------------------------------------------------------------
    // ... (منطق الثيمات والشريط الجانبي) ...
    function updateToggleIcon(theme) {
        const icon = themeToggle.querySelector('i');
        if (theme === 'dark') {
            icon.classList.remove('bi-moon-stars-fill');
            icon.classList.add('bi-sun-fill');
        } else {
            icon.classList.remove('bi-sun-fill');
            icon.classList.add('bi-moon-stars-fill');
        }
    }

    const storedTheme = localStorage.getItem('theme');
    const initialTheme = storedTheme || 'light';
    htmlElement.setAttribute('data-bs-theme', initialTheme);
    updateToggleIcon(initialTheme);

    themeToggle?.addEventListener('click', function() {
        let currentTheme = htmlElement.getAttribute('data-bs-theme');
        let newTheme = (currentTheme === 'light' || currentTheme === null) ? 'dark' : 'light';
        
        htmlElement.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateToggleIcon(newTheme);

        document.body.classList.add('animate__animated', 'animate__fadeIn');
        setTimeout(() => {
            document.body.classList.remove('animate__animated', 'animate__fadeIn');
        }, 500);
    });

    menuToggle?.addEventListener('click', function(e) {
        e.preventDefault();
        wrapper.classList.toggle('toggled');
    });

    document.querySelectorAll('.list-group-item').forEach(item => {
        item.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                wrapper.classList.remove('toggled');
            }
        });
    });

    // ------------------------------------------------------------------
    // 2. وظيفة الرسائل الموحدة (Global Alert Function)
    // ------------------------------------------------------------------

    function showAlert(message, type = 'success') {
        const alertPlaceholder = document.getElementById('alertPlaceholder');
        if (!alertPlaceholder) {
            console.warn('Alert placeholder not found. Displaying standard alert.');
            alert(message);
            return;
        }

        const wrapper = document.createElement('div');
        wrapper.innerHTML = [
            `<div class="alert alert-${type}-glass alert-dismissible fade show animate__animated animate__fadeInDown" role="alert">`,
            `   <div><i class="bi bi-info-circle-fill me-2"></i> ${message}</div>`,
            '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
            '</div>'
        ].join('');

        alertPlaceholder.prepend(wrapper);
        
        setTimeout(() => {
            wrapper.remove();
        }, 5000);
    }
    
    // جعل الدالة متاحة عالمياً
    window.showAlert = showAlert;

    // ------------------------------------------------------------------
    // 3. وظيفة الحذف الحقيقية (لجدول الطالب - schedule.html)
    // ------------------------------------------------------------------

    // يجب أن تكون دالة fetchProtectedData معرفة في management.js
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', async (event) => {
            const btn = event.currentTarget;
            const row = btn.closest('tr');
            // جلب معرف التسجيل
            const registrationId = btn.getAttribute('data-registration-id'); 

            if (!registrationId) {
                showAlert('خطأ في البيانات: معرف التسجيل غير موجود.', 'danger');
                return;
            }
            
            // تحقق أخير من وجود الدالة قبل الاستدعاء
            if (typeof fetchProtectedData !== 'function') {
                 showAlert('خطأ في النظام: لا يمكن الاتصال بالخادم (fetchProtectedData غير معرفة).', 'danger');
                 return;
            }

            if (confirm('هل أنت متأكد من حذف هذه المادة من جدولك؟')) {
                
                btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
                btn.disabled = true;

                // ⚠️ استدعاء API الحقيقي
                const response = await fetchProtectedData(`schedule/delete/${registrationId}/`, 'DELETE');

                if (response && response.detail === 'تم إلغاء التسجيل بنجاح.') {
                    // ✅ نجاح: تنفيذ أنيميشن الحذف
                    row.classList.add('animate__animated', 'animate__fadeOutRight');
                    setTimeout(() => {
                        row.remove();
                        showAlert('تم حذف المادة من جدولك بنجاح.', 'success');
                    }, 800);
                } else {
                    // ❌ فشل
                    const errorMsg = response && response.detail ? response.detail : 'حدث خطأ أثناء إلغاء التسجيل.';
                    showAlert(`فشل الحذف: ${errorMsg}`, 'danger');
                    
                    // إعادة حالة الزر
                    btn.innerHTML = '<i class="bi bi-x-circle-fill"></i> حذف';
                    btn.disabled = false;
                }
            }
        });
    });

});