# 🎓 Student Registration System — DS College of Engineering & Technology

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat-square&logo=render&logoColor=white)

</div>

A full-stack **Student Registration & Management Web Application** built with Flask and SQLAlchemy, providing separate portals for **Students** and **Administrators** to manage academic records, profiles, and registrations from a single unified system — backed by a cloud-hosted **PostgreSQL** database on **Supabase**.

<div align="center">

[![Click Here to Open 👉](https://img.shields.io/badge/Click%20Here%20to%20Open%20👉-Live%20Demo-FF6B6B?style=for-the-badge)](https://student-registration-system-and.onrender.com)
&nbsp;
[![📁 Repository](https://img.shields.io/badge/📁-View%20Repository-4ECDC4?style=for-the-badge)](https://github.com/D-Sarkar-2508/Student-Registration-System-and-Management)

</div>

> ⚠️ **Note:** The app is hosted on Render's free tier. The server may spin down after inactivity, so the first request after idling can take 30–60 seconds to respond.

---

## 📑 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Role-Based Access](#role-based-access)
6. [Usage Guide](#usage-guide)
   - [Student Portal](#-student-portal)
   - [Admin Portal](#-admin-portal)
7. [Local Setup](#local-setup)
8. [Database Setup](#database-setup)
9. [Deployment](#deployment)
10. [Author](#author)

---

## Overview

The **Student Registration System** is a clean, role-based web platform that allows students to register, log in, manage their personal and academic details, and view a digital ID card — while administrators get a centralized dashboard to manage all student records across branches and academic years.

The system enforces secure authentication (hashed passwords), input validation, and duplicate checks (roll number/email) to keep student data consistent and reliable. All data is stored in a cloud-hosted **PostgreSQL** database on **Supabase**, ensuring full persistence across server restarts and redeployments.

---

## Features

- **Two Separate Portals** — Independent login/signup flows for Students and Admins.
- **Secure Authentication** — Passwords hashed using Werkzeug security; session-based login.
- **Student Self-Service** — Students can register, log in, update their profile, and view their digital ID card.
- **Admin Dashboard** — Quick stats on total students, breakdown by year and branch, plus recently registered students.
- **Full CRUD for Students** — Admins can add, view, edit, search, filter, and delete student records.
- **Smart Search & Filters** — Search students by name, roll number, or email; filter by branch and academic year.
- **Autocomplete Login** — Login forms show a dropdown of registered users with saved credentials support.
- **Form Validation** — Server-side validation for email format, 10-digit phone numbers, password strength, and matching confirmation fields.
- **Duplicate Protection** — Prevents duplicate roll numbers, emails, and admin usernames.
- **Digital ID Card** — Students can view and print a formatted college ID card from their portal.
- **Cloud Database** — Persistent PostgreSQL database on Supabase — data survives server restarts.
- **Responsive Design** — Clean UI built with HTML5, CSS3, and JavaScript for use across devices.

---

## Tech Stack

| Layer            | Technology                                |
|------------------|-------------------------------------------|
| Backend          | Python (Flask 3.0)                        |
| ORM              | Flask-SQLAlchemy                          |
| Database         | PostgreSQL (hosted on Supabase)           |
| Authentication   | Werkzeug Security (password hashing)      |
| Frontend         | HTML5, CSS3, JavaScript, Jinja2 Templates |
| WSGI Server      | Gunicorn                                  |
| Deployment       | Render                                    |
| Version Control  | Git & GitHub                              |

---

## Project Structure

```
.
├── app.py                   # Main Flask application — routes, models, logic
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not committed to Git)
├── .gitignore               # Excludes .env, __pycache__, *.db, venv/
├── static/
│   └── css/
│       └── style.css        # Global styles
└── templates/
    ├── landing.html          # Public landing page
    ├── admin/
    │   ├── base_admin.html   # Admin layout with sidebar
    │   ├── signup.html
    │   ├── login.html
    │   ├── dashboard.html
    │   ├── students.html
    │   ├── student_form.html
    │   └── view_student.html
    └── student/
        ├── base_student.html # Student layout with sidebar
        ├── home.html
        ├── register.html
        ├── login.html
        ├── dashboard.html
        ├── update.html
        └── id_card.html
```

---

## Role-Based Access

The system supports **two user roles**, each with its own portal and permissions:

| Role        | Access Scope                                                                                  |
|-------------|-----------------------------------------------------------------------------------------------|
| **Student** | Register/log in, view dashboard, update own profile, view & print digital ID card            |
| **Admin**   | Sign up/log in, view dashboard with stats, add/edit/delete/search/filter all student records |

---

## Usage Guide

### 👨‍🎓 Student Portal

- **Register** (`/student/register`) — New students sign up by providing personal details, roll number, branch, academic year, and contact information. The form validates email format, phone number, and password strength, and blocks duplicate roll numbers/emails.
- **Login** (`/student/login`) — Returning students log in with their registered email and password. An autocomplete dropdown shows registered accounts with optional credential saving.
- **Dashboard** (`/student/dashboard`) — Displays the student's full profile summary after login.
- **Update Profile** (`/student/update`) — Students can update their phone number, blood group, guardian details, address, and password. Core academic fields (name, roll number, branch, year) can only be changed by an Admin.
- **ID Card** (`/student/id-card`) — Generates a printable digital ID card with the student's details and college information.

### 🛡️ Admin Portal

- **Sign Up** (`/admin/signup`) — Admins create an account with a unique username and email.
- **Login** (`/admin/login`) — Admins log in with username/password. Autocomplete dropdown shows all registered admin accounts.
- **Dashboard** (`/admin`) — Shows total registered students, a breakdown by academic year and branch, and the 5 most recently registered students.
- **Manage Students** (`/admin/students`) — View all students with search (by name/roll number/email) and filters (by branch/year).
- **View Student** (`/admin/students/<id>`) — View full details of an individual student.
- **Add Student** (`/admin/students/add`) — Manually register a new student on behalf of the institution.
- **Edit Student** (`/admin/students/edit/<id>`) — Update any student's details, including resetting their password.
- **Delete Student** (`/admin/students/delete/<id>`) — Remove a student record permanently (with confirmation prompt).

---

## Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/D-Sarkar-2508/Student-Registration-System-and-Management.git
   cd Student-Registration-System-and-Management
   ```

2. **Create a virtual environment & activate it**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the root directory:
   ```env
   DATABASE_URL=postgresql://postgres:YourPassword@db.xxxxxxxxxxxx.supabase.co:5432/postgres
   SECRET_KEY=your-secret-key-here
   ```

   > 🔒 Never commit your `.env` file — it is already listed in `.gitignore`.

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser and navigate to**
   ```
   http://127.0.0.1:5000
   ```

---

## Database Setup

This project uses **PostgreSQL via Supabase**. To set it up:

1. Create a free project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor → New Query**
3. Paste and run the following SQL:

```sql
CREATE TABLE public.admins (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(100)  NOT NULL,
    username      VARCHAR(50)   NOT NULL UNIQUE,
    email         VARCHAR(120)  NOT NULL UNIQUE,
    password_hash VARCHAR(200)  NOT NULL,
    created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE public.students (
    id             SERIAL PRIMARY KEY,
    roll_number    VARCHAR(20)   NOT NULL UNIQUE,
    name           VARCHAR(100)  NOT NULL,
    email          VARCHAR(120)  NOT NULL UNIQUE,
    password_hash  VARCHAR(200)  NOT NULL,
    phone          VARCHAR(15)   NOT NULL,
    age            INTEGER,
    branch         VARCHAR(100)  NOT NULL,
    year           INTEGER       NOT NULL CHECK (year BETWEEN 1 AND 4),
    blood_group    VARCHAR(5),
    guardian_name  VARCHAR(100),
    guardian_phone VARCHAR(15),
    address        VARCHAR(300),
    registered_on  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

4. Copy your **connection string** from Supabase → Settings → Database → URI tab
5. Paste it as `DATABASE_URL` in your `.env` file

---

## Deployment

The application is deployed on **Render** using Gunicorn as the WSGI server, with **Supabase PostgreSQL** as the cloud database.

**Live URL:** [https://student-registration-system-and.onrender.com](https://student-registration-system-and.onrender.com)

### Environment Variables on Render

Set these in your Render service under **Environment**:

| Key            | Value                                      |
|----------------|--------------------------------------------|
| `DATABASE_URL` | Your Supabase PostgreSQL connection string |
| `SECRET_KEY`   | A secure random string                     |

> ⚠️ **Note:** Hosted on Render's free tier — the instance spins down with inactivity, so the first request after idling may take up to 50 seconds.

---

## Author

**Ditipriya Sarkar** · [D-Sarkar-2508](https://github.com/D-Sarkar-2508)

If this project helped you, consider giving the repository a ⭐!
