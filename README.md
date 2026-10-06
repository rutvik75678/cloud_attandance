☁️ Cloud-Based Student Attendance System
A cloud-hosted attendance management platform built with Django, Django RESTFramework, and PostgreSQL hosted on Supabase. Developed as a ComputerNetworks Microproject demonstrating how a real web application communicateswith a cloud database over a network.

🎯 Objective
Digitize student attendance for colleges/institutions with a secure, role-basedsystem where all data lives in a centralized cloud database, accessible fromanywhere — replacing paper registers and offline spreadsheets.

✨ Features
Three roles, three dashboards — Admin, Teacher, Student (role-based access control)
Admin: manage Students, Teachers, Classes, Subjects (full CRUD with search,filters, pagination, delete confirmations), view all attendance, reports
Teacher: dashboard with live statistics, mark/update attendance(Class → Subject → Date → student sheet), my classes/subjects, attendancehistory, reports
Student: live attendance %, subject-wise breakdown with progress bars,present/absent statistics, low-attendance warning (below 75%), history, profile
Reports: filterable (class/subject/student/date range) with CSV and PDF export
REST API: role-scoped JSON endpoints with authentication and validation
Dark/Light theme, responsive sidebar layout (mobile drawer), live charts (Chart.js)
Integrity: duplicate attendance impossible — enforced by a PostgreSQLUNIQUE(student, subject, date) constraint, not just application code

echnology Stack
Layer	Technology
Backend	Python 3.12, Django 5.x, Django REST Framework
Database	PostgreSQL (Supabase cloud, TLS via session pooler)
Frontend	HTML5, CSS3, JavaScript, Bootstrap 5
Charts	Chart.js
PDF export	ReportLab
Deployment	Render (Django + Gunicorn + WhiteNoise), GitHub
🌐 Architecture & Networking
This project is a working demonstration of client–server communication:

Client–server architecture — browsers send HTTP requests; Django responds
DNS resolves hostnames; TCP provides reliable transport;HTTPS/TLS encrypts all traffic
Request–response model with session-cookie authentication
REST API + JSON for machine-readable access
Cloud database — Django's ORM sends SQL over an encrypted TCP connection(port 5432) to PostgreSQL running in Supabase's datacenter
Built-in explainer page (with live request metadata): /network/architecture/
Browser ──HTTPS──▶ Django (Render) ──SQL/TLS──▶ PostgreSQL (Supabase)   ▲                    │   └────HTML/JSON───────┘

🗄 Database Design (ER summary)
User (role: ADMIN/TEACHER/STUDENT)
 ├──1:1── Teacher ──M:N── Subject (junction: academics_subject_teachers)
 └──1:1── Student ──N:1── SchoolClass ──1:N── Subject
              └────────N:M────────▲
                        Attendance (student, subject, date, status, marked_by)
                        UNIQUE(student, subject, date)

Key rules: deleting a class with enrolled students is blocked (PROTECT);
deleting a student cascades their attendance; deleting a teacher unassigns
subjects (SET_NULL on the marker field preserves history).

⚙️ Installation (local)
bash
git clone <your-repo-url>
cd cloud_attendance
python -m venv venv
venv\Scripts\activate            # Windows  (source venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
copy .env.example .env           # then fill in your values (below)
python manage.py migrate
python manage.py seed_data       # demo data: 30 students, 5 subjects, 3 teachers
python manage.py runserver

🔐 Environment Variables (.env)
SECRET_KEY=your-secret-key
DEBUG=True                      # False in production
ALLOWED_HOSTS=127.0.0.1,localhost

# Supabase PostgreSQL (Session Pooler — IPv4 compatible)
DB_NAME=postgres
DB_USER=postgres.<your-project-ref>
DB_PASSWORD=<your-db-password>
DB_HOST=aws-0-<region>.pooler.supabase.com
DB_PORT=5432
Supabase configuration: create a project at supabase.com → Connect → copy
the Session Pooler string. The username is postgres.<project-ref> (note the
dot). Session pooler (port 5432) is used because direct connections are IPv6-only
while most networks are IPv4 — a real-world IPv4/IPv6 transition example.

👤 Demo Accounts (created by seed_data)
| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `Admin@1234` |
| Teachers | `teacher1` … `teacher3` | `Teacher@123` |
| Students | `ST001` … `ST030` | `Student@123` |

🔌 API Documentation
All endpoints require authentication (session cookie). Full in-app docs: /api/docs/.

Method
Endpoint
Description
Success
GET	/api/students/ · /api/students/<id>/	Students	200
GET	/api/teachers/ · /api/subjects/ · /api/classes/	Catalog	200
GET	/api/attendance/?date=&subject=&status=	Attendance (role-scoped)	200
POST	/api/attendance/	Create (Teacher/Admin)	201
PUT	/api/attendance/<id>/	Update (Teacher/Admin)	200
DELETE	/api/attendance/<id>/	Delete (Admin/owner teacher)	204

Students are read-only and scoped to their own records — server-side.

🧪 Testing
bash

python manage.py test
Covers authentication & role access, attendance marking/duplicates/calculation,
REST API CRUD + permissions, and model relationships/constraints. Tests run on
local SQLite automatically so the cloud database is never touched.