# 🚀 JobTrackr Backend — Django REST API

The backend of JobTrackr is built using Django and Django REST Framework.
It provides secure REST APIs for authentication, job application management, analytics, reminders, Kanban workflow updates, resume uploads, and AI-powered resume analysis.

---

# 🏗️ Backend Tech Stack

* Python
* Django
* Django REST Framework
* JWT Authentication
* SQLite / PostgreSQL
* Django Filters
* Media File Handling
* REST APIs

---

# 📂 Backend Structure

```bash
backend/
│
├── applications/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── services.py
│
├── authentication/
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── analytics/
│
├── reminders/
│
├── media/
│
├── jobtrackr_backend/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── requirements.txt
```

---

# 🔐 Authentication System

Implemented JWT-based authentication using Django REST Framework.

## Features

* User Registration
* User Login
* Token Authentication
* Protected APIs

---

## Authentication APIs

### Register User

```http
POST /api/auth/register/
```

### Login User

```http
POST /api/auth/login/
```

---

# 📁 Job Applications Module

Core module for tracking applications.

---

## Features

* Create Application
* Edit Application
* Delete Application
* Search Applications
* Filter Applications
* Pagination
* Resume Upload
* Notes Management
* Interview Tracking

---

# 📌 Application Model Fields

```python
company_name
job_title
status
applied_date
follow_up_date
interview_date
notes
resume
position
created_at
updated_at
```

---

# 📊 Status Workflow

Application statuses:

* APPLIED
* SCREENING
* INTERVIEW
* OFFER
* REJECTED
* WITHDRAWN

---

# 🔍 Search & Filtering

Implemented using:

* DjangoFilterBackend
* SearchFilter
* OrderingFilter

---

## Supported Features

### Search

```bash
?search=google
```

Searches:

* company_name
* job_title

---

### Filter by Status

```bash
?status=INTERVIEW
```

---

### Ordering

```bash
?ordering=applied_date
```

---

### Date Range Filtering

```bash
?start_date=2026-06-01&end_date=2026-06-30
```

---

# 📄 Resume Upload System

Supports uploading:

* PDF
* DOC
* DOCX

Using multipart/form-data requests.

---

## Media Configuration

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

---

# 📝 Notes System

Users can save:

* Interview notes
* HR feedback
* Personal reminders
* Follow-up information

---

# 📌 Activity Timeline System

Tracks all application activities.

---

## Activities Tracked

* Application Created
* Status Changed
* Resume Uploaded
* Interview Scheduled
* Notes Updated

---

# 🎯 Kanban Board APIs

Supports drag-and-drop status updates.

---

## Status Update Endpoint

```http
PATCH /api/applications/:id/status/
```

---

## Custom DRF Action

```python
@action(detail=True, methods=["patch"])
```

---

# 📊 Analytics System

Provides dashboard analytics.

---

## Features

* Total Applications
* Status Counts
* Monthly Application Trends
* Success Rate
* Upcoming Interviews

---

# 🔔 Reminder System

Tracks:

* Follow-up dates
* Interview schedules
* Upcoming reminders

---

# 📅 Calendar API

Provides calendar event data.

---

## Endpoint

```http
GET /api/applications/calendar-events/
```

---

# 🤖 AI Resume Analyzer

Analyzes resumes and extracts:

* Skills
* Strengths
* Weaknesses
* Suggestions

Supports:

* File Upload
* Text Input

---

# 🔒 Permissions & Security

Used:

```python
permission_classes = [IsAuthenticated]
```

Ensures all application data is user-specific.

---

# ⚡ API Features

## Pagination

```python
PageNumberPagination
```

---

## Filtering

```python
DjangoFilterBackend
```

---

## Searching

```python
SearchFilter
```

---

## Ordering

```python
OrderingFilter
```

---

# 🚀 Setup Instructions

# 1️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

# 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 3️⃣ Run Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

---

# 4️⃣ Start Development Server

```bash
python manage.py runserver
```

Backend URL:

```bash
http://127.0.0.1:8000
```

---

# 📦 Main Dependencies

```txt
Django
djangorestframework
djangorestframework-simplejwt
django-filter
Pillow
corsheaders
```

---

# 🌐 Main API Endpoints

## Authentication

```http
POST /api/auth/register/
POST /api/auth/login/
```

---

## Applications

```http
GET    /api/applications/
POST   /api/applications/
GET    /api/applications/:id/
PATCH  /api/applications/:id/
DELETE /api/applications/:id/
```

---

## Kanban Status Update

```http
PATCH /api/applications/:id/status/
```

---

## Calendar Events

```http
GET /api/applications/calendar-events/
```

---

## Analytics

```http
GET /api/analytics/
```

---

# 🧠 Backend Concepts Learned

* REST API Development
* JWT Authentication
* Django ViewSets
* DRF Serializers
* Filtering & Search
* File Upload Handling
* Query Optimization
* Custom DRF Actions
* Media File Serving
* User-based QuerySets
* Pagination
* Activity Logging

---

# 🚀 Future Backend Improvements

* Celery + Redis Background Tasks
* Email Notifications
* WebSocket Real-Time Updates
* AI Job Matching APIs
* Resume Parsing APIs
* Notification System
* Export APIs (CSV/Excel)
* Rate Limiting
* API Caching
* Docker Deployment
* PostgreSQL Optimization

---

# 💼 Resume Description

> Developed scalable backend APIs for an AI-powered Job Tracking platform using Django REST Framework with JWT authentication, Kanban workflow management, analytics, file uploads, activity timelines, reminders, and calendar integrations.

---

# 👨‍💻 Author

Ganesh Mirashi

Python Full Stack Developer
