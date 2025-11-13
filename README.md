<p dir="rtl" align="right">
<b>فلسطين…</b><br>
وطنٌ محاصرٌ لكنه يحاصر العالم بضميرٍ لا ينام.<br>
جراحٌ تُعلّمنا معنى الصمود، ودموعٌ تشهد أن الحرية أغلى من الحياة.<br>
لن تكون فلسطين مجرد خبر، بل ستبقى الحكاية التي تكتبها الأجيال.<br><br>
<img src="https://flagcdn.com/w40/ps.png">
</p>

# 🎓 Faculty-Academy – Production-Ready Academic Registration System  
A full Student Information System (SIS) built with **Django**, offering a complete academic registration workflow for **Students**, **Instructors**, and **Administrators**.  
The system is designed to be clean, scalable, and ready for production deployment.

---

# 🚀 Overview  
Faculty-Academy is a role-based academic management system that handles:

- Course registration  
- Student enrollment  
- Instructor grading workflow  
- Schedule management  
- Admin-level user & course management  
- Backend API for frontend consumption (Vanilla JS + Bootstrap)  

This project is built with **clean architecture principles** and follows **production-ready Django patterns**.

---

# 🧩 Features

### 👨‍🎓 Student  
- View available courses  
- Register for courses  
- Access personal schedule  
- View academic info  

### 👨‍🏫 Instructor  
- View assigned courses  
- Submit or update student grades  
- Manage course-related data  

### 🛡️ Administrator  
- Create/update/delete Courses  
- Manage Students & Instructors  
- Assign instructors to courses  
- Full admin access through Django Admin  

---

# 🏛️ Technology Stack

### Backend  
- Django 4.x  
- Django Auth (RBAC)  
- Django Templates  

### Frontend  
- HTML  
- CSS  
- Vanilla JavaScript  
- Bootstrap 5  

### Database  
- SQLite (Development)  
- PostgreSQL (Production Recommended)

---

# 🗂️ Project Structure (Production-Ready)

```
faculty_academy/
│
├── academic/                # Core project settings
│   ├── settings.py
│   ├── urls.py
│   ├── permissions.py
│   └── wsgi.py/asgi.py
│
├── students/                # Student app
├── instructors/             # Instructor app
├── admin_panel/             # Admin-level routes
│
├── static/                  # CSS, JS, images
├── templates/               # HTML templates
│   ├── login.html
│   ├── student/
│   ├── instructor/
│   └── admin/
│
└── manage.py
```

---

# 🔐 Role-Based Permissions (Production-Ready)

### **Admin**
| Endpoint | Description |
|---------|-------------|
| `/api/admin/courses/add/` | Add course |
| `/api/admin/students/` | Manage students |
| `/api/admin/instructors/add/` | Add instructor |

Permission: `is_superuser` or `is_staff`

---

### **Instructor**
| Endpoint | Description |
|---------|-------------|
| `/api/instructor/my-courses/` | View assigned courses |
| `/api/instructor/grade/update/` | Submit/update grades |

Permission: Instructor account linked to `Instructor` model

---

### **Student**
| Endpoint | Description |
|---------|-------------|
| `/api/courses/` | Register for courses |
| `/api/schedule/` | View schedule |

Permission: `IsAuthenticated`

---

# 🛠️ Installation (Local Setup)

### 1️⃣ Clone the project
```bash
git clone https://github.com/Mahmoud3310B/Faculty-Academy
cd Faculty-Academy
```

### 2️⃣ Create & activate virtual environment
```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

### 3️⃣ Install requirements
```bash
pip install -r requirements.txt
```

### 4️⃣ Apply migrations
```bash
python manage.py migrate
```

### 5️⃣ Create admin account
```bash
python manage.py createsuperuser
```

### 6️⃣ Run development server
```bash
python manage.py runserver
```

System available at:  
- Frontend Login → http://127.0.0.1:8000/login.html  
- Django Admin → http://127.0.0.1:8000/admin/  

---

# 🗄️ Database Schema Summary

### Tables:
- Student  
- Instructor  
- Course  
- Enrollment  
- Grade  
- User (Django Auth)

### Relationship Model:
- Student ↔ Enrollment ↔ Course  
- Instructor ↔ Course  
- Course ↔ Grade ↔ Student  

---

# 🧪 API Behavior (Production Notes)

All endpoints return:

```
{
  "status": "success/error",
  "message": "",
  "data": [...]
}
```

Status Codes:
- `200 OK`
- `400 Bad Request`
- `403 Forbidden`
- `404 Not Found`
- `500 Server Error`

---

# 🔧 Production Deployment (Basic Guide)

### Recommended Stack:
- Ubuntu 22.04  
- PostgreSQL  
- Nginx Reverse Proxy  
- Gunicorn  
- Supervisor for process management  
- SSL via Certbot  

Folder:
```
/var/www/faculty-academy/
```

Commands:
```bash
gunicorn academic.wsgi --bind 0.0.0.0:8001
```

Nginx will reverse-proxy → `localhost:8001`

---

# 🚀 Future Roadmap (Production Features)

- JWT Authentication  
- Full REST API with DRF  
- Student Payments Module  
- Attendance module  
- Grades analytics dashboard  
- Export transcripts (PDF)  
- Multi-instructor courses  
- Email Notifications  
- Two-Factor Authentication  

---

# 📜 License  
MIT License — free for educational and commercial use.

---

# 👨‍💻 Developer  
**Mahmoud Attia Khalifa**  
Full-Stack Developer • Django • AI • Cybersecurity  
📧 Email: mahmoud.ektra@gmail.com  
🔗 GitHub: https://github.com/Mahmoud3310B
