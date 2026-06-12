# 🎓 Student Registration & Management System — SRMS

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com)

A sleek, responsive, full-stack web application designed to streamline academic workflows and profile administration. Built with **Flask** and backed by a secure **Supabase** data layer, this platform provides multi-role authentication, interactive data tracking, and dynamic modern UI dashboards for students, faculty, and administrators.

---

## 🚀 Live Access

> 💡 **Tip:** For the best experience, please review the registration rules and dashboard workflow instructions below before accessing the system.

<p align="center">
  <a href="https://student-registration-system-and.onrender.com">
    <img src="https://img.shields.io/badge/⚡%20CLICK%20HERE%20TO%20OPEN-LIVE%20DEMO-FF5733?style=for-the-badge" alt="Live Demo">
  </a>
  <a href="https://github.com/D-Sarkar-2508/Student-Registration-System-and-Management/tree/main">
    <img src="https://img.shields.io/badge/📁%20VIEW%20REPOSITORY-MAIN%20BRANCH-008080?style=for-the-badge" alt="Repository">
  </a>
</p>

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Key Features](#-key-features)
3. [Tech Stack](#-tech-stack)
4. [Project Structure](#-project-structure)
---

## 🔍 Overview

The **Student Registration & Management System (SRMS)** replaces manual, fragmented spreadsheet tracking with an integrated single-page hub. Featuring a custom **modern dark-theme design layout with a vibrant blue-teal palette and card-style controls**, it ensures that student records, course enrollment statuses, and academic qualifications remain instantly accessible yet securely isolated across individual authorization tiers.

---

## ✨ Key Features

* **Secure Access Control:** Separate workflow paths for Students, Faculty, and Administrators with dynamic client/server-side validations.
* **Comprehensive Student Profiling:** Track explicit details including student IDs, degrees, department specializations, ongoing academic status, and core contact matrices.
* **Intuitive Registration Workflow:** Streamlined course sign-ups, schedule checks, and active enrollment logs.
* **Modern Interactive UI:** Layouts utilize uniform UI card structures and fast, asynchronous actions that minimize full-page reloads.

---

## 🛠 Tech Stack

| Architecture Layer | Component Technology |
| :--- | :--- |
| **Backend Core** | Python (Flask 3.0+) |
| **Database Engine** | Supabase (PostgreSQL Distributed Instance) |
| **Frontend Framework** | HTML5 / CSS3 (Custom Dark-Palette Matrix) / Vanilla JS |
| **Containerization** | Docker |
| **Hosting Platform** | Render Cloud Infrastructure |
| **VCS Infrastructure** | Git & GitHub |

---

## 📂 Project Structure

```text
├── app.py                 # Core application controller, route declarations & system configs
├── requirements.txt       # Project runtime dependencies
├── Dockerfile             # Container blueprint configuration for uniform hosting
├── .gitignore             # Deployment ignore patterns
├── static/                # Compiled asset delivery engine
│   ├── css/               # Modular stylesheet templates (Teal-Dark theme layout)
│   └── js/                # Client form evaluators & interactive overlay controllers
└── templates/             # Application UI blueprints
    ├── base.html          # Shell structural blueprint
    ├── index.html         # Landing selection interface
    └── dashboards/        # Segmented viewports (Student, Faculty, Admin portals)
