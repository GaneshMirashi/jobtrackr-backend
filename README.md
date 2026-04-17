# JobTrackr Backend

JobTrackr Backend is a production-ready Django REST API that powers the JobTrackr AI application — a smart job application tracking system designed to help users manage, analyze, and improve their job search process.

## 🚀 Features

- JWT-based authentication (access + refresh tokens)
- Custom user model with email login
- Job application tracking with status management
- Kanban-style workflow support (Applied → Interview → Offer, etc.)
- AI-powered resume analysis (via Gemini API)
- Background task processing for reminders (Celery + Redis)
- RESTful API design with pagination, filtering, and search

## 🏗️ Architecture

The backend follows a modular monolith architecture using Django apps:

- `accounts` → Authentication & user management  
- `applications` → Job application CRUD & status tracking  
- `resume` → Resume upload & AI analysis  
- `reminders` → Scheduled notifications & background jobs  

## 🛠️ Tech Stack

- Django 4.2+
- Django REST Framework
- SimpleJWT (Authentication)
- PostgreSQL (Production) / SQLite (Development)
- Celery + Redis (Async tasks)
- PyPDF2 (Resume parsing)
- Google Gemini API (AI integration)

## ⚙️ Setup Instructions

```bash
git clone https://github.com/<your-username>/jobtrackr-backend.git
cd jobtrackr-backend

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
