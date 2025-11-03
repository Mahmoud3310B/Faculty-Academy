# بسم الله الرحمن الرحيم وما توفيقي الا بالله متنسوش فلسطين في دعائكم ![Palestine Flag](https://flagcdn.com/w40/ps.png) 

Comprehensive Academic Registration Systemfor we Delevoper Faculty-Academy from Django 🎓
# Project Summary 🎓
This project is a comprehensive Student Information System (SIS) primarily developed with the Django framework to build a robust Backend API for data management and logic control. The frontend utilizes standard HTML/CSS/JavaScript (Vanilla JS with Bootstrap) to deliver a fast and responsive user experience. The system is designed to automate and manage registration processes, course management, grading, and fees across three key user roles: Student, Instructor, and Administrator.

# Core Features and Functionality:
<img width="1055" height="581" alt="image" src="https://github.com/user-attachments/assets/f815bf8a-a9d5-4ee6-8839-c915a9b683e1" />

# Technology Stack


<img width="1051" height="452" alt="image" src="https://github.com/user-attachments/assets/1eb2fa68-a6c0-4b62-b8c4-d13c04c6b6e7" />

# Role Structure and Key API Endpoints 

The API endpoints (defined in academic/urls.py) and permissions (in academic/permissions.py) are structured to serve specific roles:

1. Administrator:

Paths: /api/admin/courses/add/, /api/admin/students/, /api/admin/instructors/add/.

Permission: Requires is_superuser or is_staff.

2. Instructor:

Paths: /api/instructor/my-courses/, /api/instructor/grade/update/.

Permission: Requires the user to be linked to an Instructor object.

3. Student:

Paths: /api/courses/ (for registration), /api/schedule/.

Permission: Requires standard authentication (IsAuthenticated).
# Local Setup Guide (Installation) 🛠️
# Login Page Project ✨🤍

Prerequisites: Python 3.9+ and pip installed.

1. Clone the Repository:
<img width="999" height="183" alt="image" src="https://github.com/user-attachments/assets/ec47c736-ce6c-4873-bc8f-9150272c4fbd" />

2. Create and Activate Virtual Environment:

<img width="999" height="335" alt="image" src="https://github.com/user-attachments/assets/8e4614d2-cf26-4eb5-ae05-7bdf84dd68b6" />

3. Install Required Packages:

<img width="1009" height="198" alt="image" src="https://github.com/user-attachments/assets/3c3e1bae-7745-4e0d-ad34-2f543e9537c4" />

4. Run Migrations:

<img width="1009" height="178" alt="image" src="https://github.com/user-attachments/assets/7e99f99f-f3b2-4af1-a8ac-9728b5d5fa78" />
5. Create a Superuser (Admin Account):

<img width="1012" height="140" alt="image" src="https://github.com/user-attachments/assets/6573ae01-91bc-4d84-b220-5e7e5514f1d3" />

6.  Run the Server:

<img width="994" height="131" alt="image" src="https://github.com/user-attachments/assets/852bd314-9fdb-4ee9-8db0-2692a3558c7d" />

7. The system will be accessible via the Django Admin at http://127.0.0.1:8000/admin/ and the main application login page (e.g., http://127.0.0.1:8000/login.html).

Would you like me to help you draft the requirements.txt file based on the uploaded code and configurations? 


<img width="1911" height="871" alt="image" src="https://github.com/user-attachments/assets/46d51ac5-d5d8-4d88-afe5-d552347dda9d" />
